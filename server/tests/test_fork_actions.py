"""The fork's own action tools register through fork_actions and keep their own contract."""

from collections.abc import Callable

import pytest
from mcp.server.mcpserver.exceptions import ToolError

from revit_model_mcp.fork_actions import register_fork_actions


class FakeMcp:
    def __init__(self):
        self.tools: dict[str, tuple[Callable, dict]] = {}

    def tool(self, **kwargs):
        def decorate(function):
            self.tools[kwargs.get("title", function.__name__)] = (function, kwargs)
            return function

        return decorate


def registered_tool():
    mcp = FakeMcp()
    register_fork_actions(mcp, lambda command, **payload: {})
    assert set(mcp.tools) == {"Set View Lighting"}
    return next(iter(mcp.tools.values()))[0]


@pytest.mark.anyio
async def test_set_view_lighting_rejects_an_empty_change():
    tool = registered_tool()
    with pytest.raises(ToolError, match="at least one lighting setting"):
        await tool(view="1")


@pytest.mark.anyio
async def test_set_view_lighting_requires_paired_sun_angles():
    tool = registered_tool()
    with pytest.raises(ToolError, match="must be provided together"):
        await tool(view="1", sun_azimuth_deg=135)


@pytest.mark.anyio
async def test_set_view_lighting_sends_a_sparse_fork_bag():
    seen: dict = {}

    async def send(command: str, **payload):
        seen["command"] = command
        seen.update(payload)
        return {"ok": True}

    mcp = FakeMcp()
    register_fork_actions(mcp, send)
    function = next(iter(mcp.tools.values()))[0]
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
    tool = registered_tool()
    with pytest.raises(ToolError, match="gradient"):
        await tool(view="1", background="sky", background_colors=["#111111", "#222222", "#333333"])


@pytest.fixture
def anyio_backend():
    return "asyncio"


def test_set_view_lighting_is_listed_by_the_server():
    import asyncio

    from revit_model_mcp import server as revit_server

    tools = {tool.name: tool for tool in asyncio.run(revit_server.mcp.list_tools())}
    assert "revit_set_view_lighting" in tools
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
