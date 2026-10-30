"""The fork's own tools register through fork_actions and keep their own contract."""

import asyncio
from collections.abc import Callable

import pytest
from mcp.server.mcpserver.exceptions import ToolError

from revit_model_mcp.fork_actions import register_fork_actions, register_fork_reads


class FakeMcp:
    def __init__(self):
        self.tools: dict[str, tuple[Callable, dict]] = {}

    def tool(self, **kwargs):
        def decorate(function):
            self.tools[function.__name__] = (function, kwargs)
            return function

        return decorate


def registered_tools():
    mcp = FakeMcp()
    register_fork_actions(mcp, lambda command, **payload: {})
    register_fork_reads(mcp, lambda job, timeout, document: {})
    return {name: function for name, (function, _) in mcp.tools.items()}


def tool(name: str):
    return registered_tools()[name]


def test_every_fork_tool_is_registered():
    assert set(registered_tools()) == {
        "revit_set_view_lighting",
        "revit_create_level",
        "revit_create_floor",
        "revit_set_phase",
        "revit_merge_phases",
        "revit_reset_element_ids",
        "revit_rebuild_model_ids",
        "revit_export_element_ids",
    }


@pytest.mark.anyio
async def test_set_view_lighting_rejects_an_empty_change():
    with pytest.raises(ToolError, match="at least one lighting setting"):
        await tool("revit_set_view_lighting")(view="1")


@pytest.mark.anyio
async def test_set_view_lighting_requires_paired_sun_angles():
    with pytest.raises(ToolError, match="must be provided together"):
        await tool("revit_set_view_lighting")(view="1", sun_azimuth_deg=135)


@pytest.mark.anyio
async def test_set_view_lighting_sends_a_sparse_fork_bag():
    seen: dict = {}

    async def send(command: str, **payload):
        seen["command"] = command
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_set_view_lighting"][0]
    result = await function(
        view="Level 1",
        shadows=True,
        sun_date="2026-03-01",
        sun_time="10:30",
        dry_run=True,
    )
    assert result == {"ok": True}
    assert seen["command"] == "set-view-lighting"
    assert seen["view"] == "Level 1"
    assert seen["dryRun"] is True
    # Only the settings the caller passed reach the add-in, so an absent key means "leave it alone".
    assert seen["fork"] == {"shadows": True, "sunDate": "2026-03-01", "sunTime": "10:30"}


@pytest.mark.anyio
async def test_set_view_lighting_colors_need_a_gradient_background():
    with pytest.raises(ToolError, match="gradient"):
        await tool("revit_set_view_lighting")(
            view="1", background="sky", background_colors=["#111111", "#222222", "#333333"]
        )


@pytest.mark.anyio
async def test_create_level_sends_its_elevation_in_the_fork_bag():
    seen: dict = {}

    async def send(command: str, **payload):
        seen["command"] = command
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_create_level"][0]
    await function(name="L3", elevation_mm=9000.5, create_view=True, dry_run=False)

    assert seen["command"] == "create-level"
    assert seen["name"] == "L3"
    assert seen["fork"] == {"elevationMm": 9000.5, "createView": True}


@pytest.mark.anyio
async def test_create_floor_sends_the_closed_boundary():
    seen: dict = {}

    async def send(command: str, **payload):
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_create_floor"][0]
    await function(points_mm=[[0, 0], [4000, 0], [4000, 3000]], level="L1", floor_type="Floor-Slab")

    assert seen["pointsMm"] == [[0, 0], [4000, 0], [4000, 3000]]
    assert seen["level"] == "L1"
    assert seen["fork"] == {"floorType": "Floor-Slab"}


@pytest.mark.anyio
async def test_create_floor_refuses_a_repeated_vertex():
    with pytest.raises(ToolError, match="must not repeat consecutively"):
        await tool("revit_create_floor")(points_mm=[[0, 0], [0, 0], [4000, 0]], level="L1")


@pytest.mark.anyio
async def test_set_phase_needs_one_of_the_two_phases():
    with pytest.raises(ToolError, match="At least one of"):
        await tool("revit_set_phase")(element_ids=[42])


@pytest.mark.anyio
async def test_set_phase_keeps_an_empty_name_to_clear_a_phase():
    seen: dict = {}

    async def send(command: str, **payload):
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_set_phase"][0]
    await function(element_ids=[42, 43], created_phase="", demolished_phase="Existing")

    assert seen["elementIds"] == [42, 43]
    # An empty string means "clear"; only null means "leave it alone".
    assert seen["fork"] == {"createdPhase": "", "demolishedPhase": "Existing"}


@pytest.mark.anyio
async def test_set_phase_refuses_a_blank_but_non_empty_name():
    with pytest.raises(ToolError, match="empty string to clear"):
        await tool("revit_set_phase")(element_ids=[42], created_phase="   ")


@pytest.mark.anyio
async def test_merge_phases_refuses_the_same_phase_twice():
    with pytest.raises(ToolError, match="must differ"):
        await tool("revit_merge_phases")(source_phase="Phase 1", target_phase="phase 1")


@pytest.mark.anyio
async def test_reset_element_ids_sends_the_addresses_without_a_fork_bag():
    seen: dict = {}

    async def send(command: str, **payload):
        seen["command"] = command
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_reset_element_ids"][0]
    await function(element_ids=[7, 8], dry_run=True)

    assert seen["command"] == "reset-element-ids"
    assert seen["elementIds"] == [7, 8]
    assert seen["dryRun"] is True
    assert "fork" not in seen


@pytest.mark.anyio
async def test_rebuild_model_ids_carries_the_destination_in_the_fork_bag():
    seen: dict = {}

    async def send(command: str, **payload):
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_rebuild_model_ids"][0]
    await function(destination_path=r"C:\out\model.rvt", copies=2, seed=7, view="3D")

    assert seen["view"] == "3D"
    assert seen["fork"] == {
        "destinationPath": r"C:\out\model.rvt",
        "overwrite": False,
        "removeTemplateLevels": True,
        "seed": 7,
        "duplicateNames": "override",
        "copies": 2,
    }
    # The destination belongs to the fork bag: it is not one of upstream's action fields.
    assert "destinationPath" not in seen


@pytest.mark.anyio
async def test_export_element_ids_reads_through_the_read_dispatcher():
    seen: dict = {}

    async def execute(job, timeout_seconds, document):
        seen["command"] = job.command
        seen["payload"] = job.payload
        seen["timeout"] = timeout_seconds
        seen["document"] = document
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_reads(mcp, execute)
    function = mcp.tools["revit_export_element_ids"][0]
    result = await function(fields=["category", "id"], path=r"C:\out\ids.xlsx", document="Model")

    assert result == {"ok": True}
    assert seen["command"] == "export-element-ids"
    assert seen["payload"] == {
        "command": "export-element-ids",
        "fields": ["category", "id"],
        "saveTo": r"C:\out\ids.xlsx",
    }
    assert seen["document"] == "Model"


def test_fork_tools_are_listed_by_the_server():
    from revit_model_mcp import server as revit_server

    tools = {tool.name: tool for tool in asyncio.run(revit_server.mcp.list_tools())}
    assert {
        "revit_set_view_lighting",
        "revit_create_level",
        "revit_create_floor",
        "revit_set_phase",
        "revit_merge_phases",
        "revit_reset_element_ids",
        "revit_rebuild_model_ids",
        "revit_export_element_ids",
    } <= set(tools)

    properties = tools["revit_set_view_lighting"].input_schema["properties"]
    assert set(properties) == {
        "view",
        "shadows",
        "shadow_intensity",
        "sunlight_intensity",
        "sun_date",
        "sun_time",
        "sun_azimuth_deg",
        "sun_altitude_deg",
        "ground_plane",
        "ground_plane_level",
        "background",
        "background_colors",
        "lighting_scheme",
        "dry_run",
        "document",
    }
    assert set(tools["revit_create_level"].input_schema["properties"]) == {
        "name",
        "elevation_mm",
        "create_view",
        "dry_run",
        "document",
    }
    assert set(tools["revit_export_element_ids"].input_schema["properties"]) == {
        "fields",
        "path",
        "timeout_seconds",
        "document",
    }
    # The register is a read: it stays listed and usable while the workstation is read-only.
    assert tools["revit_export_element_ids"].annotations.read_only_hint is True


@pytest.fixture
def anyio_backend():
    return "asyncio"
