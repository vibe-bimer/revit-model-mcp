"""The fork's own action tools.

Fork actions register here instead of inside ``actions.py``, so upstream changes cannot
collide with them. Each tool goes through the same ``send`` coroutine ``actions.py`` closes
over (the policy gate and the client-identity wrapper included), never around it. See
``adr/0005`` for the seam and ``adr/0001`` for the base.
"""

from typing import Annotated, Any, Literal

from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

from revit_model_mcp.revit_channel import with_client_identity

Number = Annotated[float, Field(allow_inf_nan=False)]
Name = Annotated[str, Field(min_length=1)]


def register_fork_actions(mcp, send) -> None:
    """Registers the fork's extra action tools onto the shared MCP server."""

    @mcp.tool(
        title="Set View Lighting",
        annotations=ToolAnnotations(
            title="Set View Lighting",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_set_view_lighting(
        view: Name,
        shadows: bool | None = None,
        shadow_intensity: Annotated[int, Field(ge=0, le=100)] | None = None,
        sunlight_intensity: Annotated[int, Field(ge=0, le=100)] | None = None,
        sun_date: str | None = None,
        sun_time: str | None = None,
        sun_azimuth_deg: Number | None = None,
        sun_altitude_deg: Number | None = None,
        ground_plane: bool | None = None,
        ground_plane_level: Name | None = None,
        background: Literal["sky", "gradient"] | None = None,
        background_colors: Annotated[list[str], Field(min_length=3, max_length=3)] | None = None,
        lighting_scheme: Literal[
            "exterior-sun",
            "exterior-sun-and-artificial",
            "exterior-artificial",
            "interior-sun",
            "interior-sun-and-artificial",
            "interior-artificial",
        ]
        | None = None,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Set the lighting of one view: shadows, sun position, ground plane, background and the rendering lighting scheme.

        `view` is an exact non-template view name or its decimal view ID, as revit_list_views reports it; a view without sun and shadow settings is refused.
        Every other argument is optional and only the ones you pass change; the response reports the readings before and after under verification.before.lighting and verification.after.lighting, and names what moved in changedSettings.
        `shadows` switches the view's per-view sun and shadow display: with it off Revit draws neither the sun path nor cast shadows, so the intensity settings stop showing; Revit exposes no API for the Graphic Display Options Shadows checkbox, so this per-view switch is the only shadow switch the tool can write, and a view whose sun and shadow settings are shared is refused.
        `shadow_intensity` is 0 (no cast shadow) to 100 (black) and `sunlight_intensity` is 0 to 100.
        `sun_date` (yyyy-MM-dd) and `sun_time` (24-hour HH:mm) fix a still-image sun position and are handed to Revit as local time; the readings report the stored instant as sunDateAndTimeUtc with the project time zone. Passing one keeps the other half, and both switch a sun study back to a still image.
        `sun_azimuth_deg` (clockwise from north) and `sun_altitude_deg` (degrees above the horizon) set a fixed lighting-study sun instead, and must be passed together.
        `ground_plane` uses the ground plane and `ground_plane_level` names its level; a level Revit does not already hold as a ground plane is marked as one and the response says so.
        `background` is `sky` or `gradient` and works on 3D, section and elevation views; `background_colors` gives the three gradient colors as #RRGGBB (sky, horizon, ground).
        `lighting_scheme` sets the rendering lighting source: exterior-sun, exterior-sun-and-artificial, exterior-artificial, interior-sun, interior-sun-and-artificial or interior-artificial.
        Sun and shadow settings belong to the view; a view that shares them reports sunSettingsShared true and passes the change on to every view that shares them.
        dry_run executes and rolls back, returning the same verification block without changing the model.
        `document` addresses one specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        settings: dict[str, Any] = {
            "shadows": shadows,
            "shadowIntensity": shadow_intensity,
            "sunlightIntensity": sunlight_intensity,
            "sunDate": sun_date,
            "sunTime": sun_time,
            "sunAzimuthDeg": sun_azimuth_deg,
            "sunAltitudeDeg": sun_altitude_deg,
            "groundPlane": ground_plane,
            "groundPlaneLevel": ground_plane_level,
            "background": background,
            "lightingScheme": lighting_scheme,
        }
        if all(value is None for value in settings.values()):
            raise ToolError("Provide at least one lighting setting to change.")
        if (sun_azimuth_deg is None) != (sun_altitude_deg is None):
            raise ToolError("sun_azimuth_deg and sun_altitude_deg must be provided together.")
        if background_colors is not None and background != "gradient":
            raise ToolError("background_colors requires background 'gradient'.")
        settings["backgroundColors"] = background_colors
        # Only what the caller passed travels: the add-in reads a sparse bag, so an absent key means
        # "leave this setting alone" rather than "set it to null" (adr/0005).
        fork = {name: value for name, value in settings.items() if value is not None}
        return await send(
            "set-view-lighting", view=view, fork=fork, dryRun=dry_run, document=document
        )
