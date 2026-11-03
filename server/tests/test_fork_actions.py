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
        "revit_create_grid",
        "revit_create_column",
        "revit_create_beam",
        "revit_load_family_file",
        "revit_place_hosted_family",
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
async def test_create_grid_sends_its_curve_in_the_fork_bag():
    seen: dict = {}

    async def send(command: str, **payload):
        seen["command"] = command
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_create_grid"][0]
    await function(label="A", start_mm=[0, 0], end_mm=[30000, 0], dry_run=True)

    assert seen["command"] == "create-grid"
    assert seen["name"] == "A"
    assert seen["fork"] == {"startMm": [0, 0], "endMm": [30000, 0]}
    assert seen["dryRun"] is True


@pytest.mark.anyio
async def test_create_grid_sends_the_arc_mid_point_when_given():
    seen: dict = {}

    async def send(command: str, **payload):
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_create_grid"][0]
    await function(label="B", start_mm=[0, 0], end_mm=[30000, 0], mid_mm=[15000, 4000])

    assert seen["fork"] == {"startMm": [0, 0], "endMm": [30000, 0], "midMm": [15000, 4000]}


@pytest.mark.anyio
async def test_create_grid_refuses_degenerate_geometry():
    with pytest.raises(ToolError, match="must not be the same point"):
        await tool("revit_create_grid")(label="A", start_mm=[0, 0], end_mm=[0, 0])
    with pytest.raises(ToolError, match="must differ from"):
        await tool("revit_create_grid")(
            label="A", start_mm=[0, 0], end_mm=[30000, 0], mid_mm=[0, 0]
        )
    with pytest.raises(ToolError, match="collinear"):
        await tool("revit_create_grid")(
            label="A", start_mm=[0, 0], end_mm=[30000, 0], mid_mm=[15000, 0]
        )


@pytest.mark.anyio
async def test_create_column_sends_its_point_at_the_top_level_and_its_top_in_the_fork_bag():
    seen: dict = {}

    async def send(command: str, **payload):
        seen["command"] = command
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_create_column"][0]
    await function(
        family="M_Concrete-Column",
        level="1F",
        x_mm=3000,
        y_mm=4500,
        type_name="600x600",
        top_level="3F",
        base_offset_mm=-150,
        dry_run=True,
    )

    assert seen["command"] == "create-column"
    assert seen["family"] == "M_Concrete-Column"
    assert seen["typeName"] == "600x600"
    assert seen["level"] == "1F"
    assert seen["xMm"] == 3000
    assert seen["yMm"] == 4500
    assert seen["fork"] == {"topLevel": "3F", "baseOffsetMm": -150, "topOffsetMm": 0}
    assert seen["dryRun"] is True


@pytest.mark.anyio
async def test_create_column_falls_back_to_a_3000_mm_height_when_no_top_is_named():
    seen: dict = {}

    async def send(command: str, **payload):
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_create_column"][0]
    await function(family="M_Concrete-Column", level="1F", x_mm=0, y_mm=0)

    assert seen["fork"] == {"baseOffsetMm": 0, "topOffsetMm": 0, "heightMm": 3000}


@pytest.mark.anyio
async def test_create_column_refuses_a_height_that_is_not_positive():
    with pytest.raises(ToolError, match="height_mm must be a positive number"):
        await tool("revit_create_column")(
            family="M_Concrete-Column", level="1F", x_mm=0, y_mm=0, height_mm=0
        )


@pytest.mark.anyio
async def test_place_hosted_family_sends_its_point_at_the_top_level_and_the_search_in_the_fork_bag():
    seen: dict = {}

    async def send(command: str, **payload):
        seen["command"] = command
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_place_hosted_family"][0]
    await function(
        family="Single-Flush",
        x_mm=3000,
        y_mm=4500,
        type_name="0900 x 2100",
        host_element_id=101,
        host_search_radius_mm=1500,
        level="1F",
        dry_run=True,
    )

    assert seen["command"] == "place-hosted-family"
    assert seen["family"] == "Single-Flush"
    assert seen["typeName"] == "0900 x 2100"
    assert seen["level"] == "1F"
    assert seen["xMm"] == 3000
    assert seen["yMm"] == 4500
    assert seen["fork"] == {"hostSearchRadiusMm": 1500, "hostElementId": 101}
    assert seen["dryRun"] is True


@pytest.mark.anyio
async def test_place_hosted_family_sends_the_default_radius_and_leaves_the_host_unset():
    seen: dict = {}

    async def send(command: str, **payload):
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_place_hosted_family"][0]
    await function(family="Single-Flush", x_mm=0, y_mm=0)

    # A sparse bag: an absent key means "leave this input alone", so a null sill or flip never travels.
    assert seen["fork"] == {"hostSearchRadiusMm": 2000}
    assert seen["level"] is None
    assert seen["rotationDeg"] == 0


@pytest.mark.anyio
async def test_place_hosted_family_carries_the_sill_and_the_flip_when_given():
    seen: dict = {}

    async def send(command: str, **payload):
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_place_hosted_family"][0]
    await function(family="Single-Flush", x_mm=0, y_mm=0, sill_height_mm=900, flip_facing=False)

    assert seen["fork"] == {"hostSearchRadiusMm": 2000, "sillHeightMm": 900, "flipFacing": False}
    assert seen["rotationDeg"] == 0


@pytest.mark.anyio
async def test_place_hosted_family_refuses_a_rotation_because_its_host_wall_decides_it():
    with pytest.raises(ToolError, match="takes its orientation from its host wall"):
        await tool("revit_place_hosted_family")(
            family="Single-Flush", x_mm=0, y_mm=0, rotation_deg=90
        )


@pytest.mark.anyio
async def test_place_hosted_family_refuses_a_search_radius_that_is_not_positive():
    with pytest.raises(ToolError, match="host_search_radius_mm must be a positive number"):
        await tool("revit_place_hosted_family")(
            family="Single-Flush", x_mm=0, y_mm=0, host_search_radius_mm=0
        )


@pytest.mark.anyio
async def test_create_beam_sends_its_axis_in_the_fork_bag():
    seen: dict = {}

    async def send(command: str, **payload):
        seen["command"] = command
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_create_beam"][0]
    await function(
        family="M_Concrete-Rectangular Beam",
        level="2F",
        start_mm=[0, 0],
        end_mm=[6000, 0],
        structural_usage="Girder",
        z_offset_mm=-150,
    )

    assert seen["command"] == "create-beam"
    assert seen["family"] == "M_Concrete-Rectangular Beam"
    assert seen["level"] == "2F"
    assert seen["fork"] == {
        "startMm": [0, 0],
        "endMm": [6000, 0],
        "structuralUsage": "Girder",
        "zOffsetMm": -150,
    }


@pytest.mark.anyio
async def test_create_beam_zeroes_the_offset_and_leaves_the_usage_out_when_absent():
    seen: dict = {}

    async def send(command: str, **payload):
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_create_beam"][0]
    await function(
        family="M_Concrete-Rectangular Beam", level="2F", start_mm=[0, 0], end_mm=[6000, 0]
    )

    assert seen["fork"] == {"startMm": [0, 0], "endMm": [6000, 0], "zOffsetMm": 0}


@pytest.mark.anyio
async def test_create_beam_refuses_an_axis_that_is_a_single_point():
    with pytest.raises(ToolError, match="start_mm and end_mm must not be the same point"):
        await tool("revit_create_beam")(
            family="M_Concrete-Rectangular Beam", level="2F", start_mm=[0, 0], end_mm=[0, 0]
        )


@pytest.mark.anyio
async def test_load_family_file_sends_its_path_in_the_fork_bag():
    seen: dict = {}

    async def send(command: str, **payload):
        seen["command"] = command
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_load_family_file"][0]
    await function(path=r"C:\lib\M_Door.rfa")

    assert seen["command"] == "load-family-file"
    assert seen["fork"] == {"path": r"C:\lib\M_Door.rfa"}
    assert seen["dryRun"] is False


@pytest.mark.anyio
async def test_load_family_file_names_the_type_and_the_overwrite_answer_when_given():
    seen: dict = {}

    async def send(command: str, **payload):
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = mcp.tools["revit_load_family_file"][0]
    await function(path=r"C:\lib\M_Door.rfa", type_name="0900 x 2100", overwrite_parameters=True)

    assert seen["fork"] == {
        "path": r"C:\lib\M_Door.rfa",
        "typeName": "0900 x 2100",
        "overwriteParameters": True,
    }


@pytest.mark.anyio
async def test_load_family_file_refuses_a_path_that_is_not_a_family_file():
    with pytest.raises(ToolError, match="must name a .rfa"):
        await tool("revit_load_family_file")(path=r"C:\lib\notes.txt")


@pytest.mark.anyio
async def test_a_family_step_sends_its_path_in_the_fork_bag():
    from revit_model_mcp.fork_actions import step_payload

    payload = step_payload(
        "load_family_file",
        {
            "path": r"C:\lib\M_Door.rfa",
            "type_name": "0900 x 2100",
            "overwrite_parameters": False,
            "dry_run": True,
        },
    )
    # A step keeps every value the caller wrote, so an explicit false travels as false; the tool
    # omits it instead, and the add-in reads both the same way.
    assert payload == {
        "command": "load-family-file",
        "fork": {
            "path": r"C:\lib\M_Door.rfa",
            "typeName": "0900 x 2100",
            "overwriteParameters": False,
        },
        "dryRun": True,
    }


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
        "revit_create_grid",
        "revit_create_column",
        "revit_create_beam",
        "revit_load_family_file",
        "revit_place_hosted_family",
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
    assert set(tools["revit_create_grid"].input_schema["properties"]) == {
        "label",
        "start_mm",
        "end_mm",
        "mid_mm",
        "dry_run",
        "document",
    }
    assert set(tools["revit_create_column"].input_schema["properties"]) == {
        "family",
        "level",
        "x_mm",
        "y_mm",
        "type_name",
        "top_level",
        "height_mm",
        "base_offset_mm",
        "top_offset_mm",
        "rotation_deg",
        "dry_run",
        "document",
    }
    assert set(tools["revit_create_beam"].input_schema["properties"]) == {
        "family",
        "level",
        "start_mm",
        "end_mm",
        "type_name",
        "structural_usage",
        "z_offset_mm",
        "dry_run",
        "document",
    }
    assert set(tools["revit_load_family_file"].input_schema["properties"]) == {
        "path",
        "type_name",
        "overwrite_parameters",
        "dry_run",
        "document",
    }
    assert set(tools["revit_place_hosted_family"].input_schema["properties"]) == {
        "family",
        "type_name",
        "x_mm",
        "y_mm",
        "host_element_id",
        "host_search_radius_mm",
        "level",
        "rotation_deg",
        "sill_height_mm",
        "flip_facing",
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


# A fork action is also a legal step of revit_run_actions, so the step table and the tool of the same
# name must describe the same inputs; drift between them is the failure this test exists for.
def test_step_fields_match_the_tool_of_the_same_name():
    from revit_model_mcp import server as revit_server
    from revit_model_mcp.fork_actions import STEP_FIELDS

    tools = {tool.name: tool for tool in asyncio.run(revit_server.mcp.list_tools())}
    for action, fields in STEP_FIELDS.items():
        tool_names = set(tools[f"revit_{action}"].input_schema["properties"])
        assert set(fields) | {"dry_run"} == tool_names - {"document"}, action


def test_a_fork_action_runs_as_a_batch_step():
    from revit_model_mcp.actions import ActionStep

    step = ActionStep(
        action="create_level",
        args={"name": "L2", "elevation_mm": 4000, "create_view": True},
    )
    assert step.payload() == {
        "command": "create-level",
        "name": "L2",
        "dryRun": False,
        "fork": {"elevationMm": 4000.0, "createView": True},
    }


def test_a_grid_step_names_the_grid_at_the_top_level():
    from revit_model_mcp.actions import ActionStep

    step = ActionStep(
        action="create_grid",
        args={"label": "A", "start_mm": [0, 0], "end_mm": [30000, 0], "mid_mm": [15000, 4000]},
    )
    assert step.payload() == {
        "command": "create-grid",
        "name": "A",
        "dryRun": False,
        "fork": {"startMm": [0, 0], "endMm": [30000, 0], "midMm": [15000, 4000]},
    }


def test_a_beam_step_keeps_its_axis_in_the_fork_bag():
    from revit_model_mcp.actions import ActionStep

    step = ActionStep(
        action="create_beam",
        args={
            "family": "M_Concrete-Rectangular Beam",
            "level": "2F",
            "start_mm": [0, 0],
            "end_mm": [6000, 0],
        },
    )
    assert step.payload() == {
        "command": "create-beam",
        "family": "M_Concrete-Rectangular Beam",
        "typeName": None,
        "level": "2F",
        "dryRun": False,
        "fork": {"startMm": [0, 0], "endMm": [6000, 0], "zOffsetMm": 0},
    }


def test_a_column_step_keeps_its_point_at_the_top_level():
    from revit_model_mcp.actions import ActionStep

    step = ActionStep(
        action="create_column",
        args={
            "family": "M_Concrete-Column",
            "level": "1F",
            "x_mm": 3000,
            "y_mm": 4500,
            "top_level": "3F",
        },
    )
    assert step.payload() == {
        "command": "create-column",
        "family": "M_Concrete-Column",
        "typeName": None,
        "level": "1F",
        "xMm": 3000,
        "yMm": 4500,
        "rotationDeg": 0,
        "dryRun": False,
        "fork": {"topLevel": "3F", "baseOffsetMm": 0, "topOffsetMm": 0},
    }


def test_a_hosted_family_step_keeps_its_host_search_in_the_fork_bag():
    from revit_model_mcp.actions import ActionStep

    step = ActionStep(
        action="place_hosted_family",
        args={
            "family": "Single-Flush",
            "x_mm": 3000,
            "y_mm": 4500,
            "host_element_id": 101,
        },
    )
    assert step.payload() == {
        "command": "place-hosted-family",
        "family": "Single-Flush",
        "typeName": None,
        "level": None,
        "xMm": 3000,
        "yMm": 4500,
        "rotationDeg": 0,
        "dryRun": False,
        "fork": {"hostSearchRadiusMm": 2000, "hostElementId": 101},
    }


def test_a_lighting_step_sends_a_sparse_fork_bag():
    from revit_model_mcp.actions import ActionStep

    step = ActionStep(
        action="set_view_lighting",
        args={"view": "L1", "shadows": True, "sun_date": "2026-03-01"},
    )
    assert step.payload() == {
        "command": "set-view-lighting",
        "view": "L1",
        "dryRun": False,
        "fork": {"shadows": True, "sunDate": "2026-03-01"},
    }


def test_a_reset_step_takes_no_fork_bag():
    from revit_model_mcp.actions import ActionStep

    step = ActionStep(action="reset_element_ids", args={"element_ids": [42, 43]})
    assert step.payload() == {
        "command": "reset-element-ids",
        "elementIds": [42, 43],
        "dryRun": False,
    }


def test_a_rebuild_step_names_its_destination_in_the_fork_bag():
    from revit_model_mcp.actions import ActionStep

    step = ActionStep(
        action="rebuild_model_ids",
        args={"destination_path": r"C:\out\model.rvt", "copies": 2},
    )
    payload = step.payload()
    assert payload["view"] == ""
    assert payload["fork"] == {
        "destinationPath": r"C:\out\model.rvt",
        "overwrite": False,
        "removeTemplateLevels": True,
        "seed": 0,
        "duplicateNames": "override",
        "copies": 2,
    }


@pytest.mark.parametrize(
    "action,args,message",
    [
        (
            "set_view_lighting",
            {"view": "L1"},
            "Provide at least one lighting setting to change.",
        ),
        (
            "set_view_lighting",
            {"view": "L1", "sun_azimuth_deg": 90},
            "sun_azimuth_deg and sun_altitude_deg must be provided together.",
        ),
        (
            "create_floor",
            {"points_mm": [[0, 0], [0, 0], [100, 0]], "level": "L1"},
            "Floor boundary points must not repeat consecutively.",
        ),
        (
            "set_phase",
            {"element_ids": [42]},
            "At least one of created_phase or demolished_phase is required.",
        ),
        (
            "merge_phases",
            {"source_phase": "Phase 1", "target_phase": "phase 1"},
            "source_phase and target_phase must differ.",
        ),
    ],
)
def test_a_fork_step_makes_the_same_refusals_as_its_tool(action, args, message):
    from revit_model_mcp.actions import ActionStep

    with pytest.raises(ValueError, match=message):
        ActionStep(action=action, args=args)


@pytest.fixture
def anyio_backend():
    return "asyncio"
