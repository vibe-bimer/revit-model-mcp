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

from revit_model_mcp.revit_channel import DEFAULT_TIMEOUT_SECONDS, Job, with_client_identity

Number = Annotated[float, Field(allow_inf_nan=False)]
Name = Annotated[str, Field(min_length=1)]
ElementId = Annotated[int, Field(strict=True, gt=0, le=9223372036854775807)]
Point = Annotated[list[Number], Field(min_length=2, max_length=2)]
ElementIds = Annotated[list[ElementId], Field(min_length=1)]
Points = Annotated[list[Point], Field(min_length=3)]


def _camel(key: str) -> str:
    first, *rest = key.split("_")
    return first + "".join(part.title() for part in rest)


def _check_floor_points(points_mm, refuse) -> None:
    """Consecutive duplicate vertices close no boundary, so a tool and a batch step both refuse them."""
    for index, point in enumerate(points_mm):
        neighbor = points_mm[(index + 1) % len(points_mm)]
        if point[0] == neighbor[0] and point[1] == neighbor[1]:
            raise refuse("Floor boundary points must not repeat consecutively.")


def _check_grid_points(start_mm, end_mm, mid_mm, refuse) -> None:
    if start_mm == end_mm:
        raise refuse("start_mm and end_mm must not be the same point.")
    if mid_mm is None:
        return
    if mid_mm in (start_mm, end_mm):
        raise refuse("mid_mm must differ from start_mm and end_mm.")
    cross = (mid_mm[0] - start_mm[0]) * (end_mm[1] - start_mm[1]) - (mid_mm[1] - start_mm[1]) * (
        end_mm[0] - start_mm[0]
    )
    if abs(cross) <= 1e-9:
        raise refuse(
            "start_mm, mid_mm and end_mm must not be collinear: an arc needs a mid point off the start-end line."
        )


def _check_beam(start_mm, end_mm, refuse) -> None:
    """A beam's axis is the whole input, so an axis of zero length is a typo, not a beam."""
    if start_mm == end_mm:
        raise refuse("start_mm and end_mm must not be the same point.")


def _check_column(height_mm, refuse) -> None:
    """A height is a length above the base, so zero or a negative number is a typo, not a column."""
    if height_mm is not None and height_mm <= 0:
        raise refuse("height_mm must be a positive number.")


def _check_hosted(host_search_radius_mm, rotation_deg, refuse) -> None:
    """A search radius is a length, so zero or a negative number is a typo, not a search."""
    if host_search_radius_mm <= 0:
        raise refuse("host_search_radius_mm must be a positive number.")
    if rotation_deg != 0:
        raise refuse(
            "A one-level hosted family takes its orientation from its host wall, so rotation_deg "
            "must be 0; use flip_facing to turn the family around."
        )


def _check_family_path(path, refuse) -> None:
    """A family load reads a .rfa; anything else is a typo worth refusing before the model is touched."""
    if not path.casefold().endswith(".rfa"):
        raise refuse("path must name a .rfa family file.")


def _check_phase_assignment(created_phase, demolished_phase, refuse) -> None:
    if created_phase is None and demolished_phase is None:
        raise refuse("At least one of created_phase or demolished_phase is required.")
    for label, value in (
        ("created_phase", created_phase),
        ("demolished_phase", demolished_phase),
    ):
        # An empty string clears the phase; anything blank but non-empty is a typo, not a name.
        if value is not None and value != "" and not value.strip():
            raise refuse(f"{label} must be a phase name, an empty string to clear, or null.")


def _check_phases_differ(source_phase, target_phase, refuse) -> None:
    if source_phase.strip().casefold() == target_phase.strip().casefold():
        raise refuse("source_phase and target_phase must differ.")


def _check_lighting(settings: dict[str, Any], refuse) -> None:
    if all(value is None for value in settings.values()):
        raise refuse("Provide at least one lighting setting to change.")
    if (settings["sunAzimuthDeg"] is None) != (settings["sunAltitudeDeg"] is None):
        raise refuse("sun_azimuth_deg and sun_altitude_deg must be provided together.")
    if settings["backgroundColors"] is not None and settings["background"] != "gradient":
        raise refuse("background_colors requires background 'gradient'.")


# A fork action also runs as one step of upstream's revit_run_actions: the step vocabulary is extended
# once, here, rather than by forking the batch tool (adr/0004, adr/0008). These are the same inputs the
# tool of the same name takes, minus document, which addresses the batch rather than the step.
STEP_FIELDS: dict[str, dict[str, tuple[Any, Any]]] = {
    "set_view_lighting": {
        "view": (Name, ...),
        "shadows": (bool | None, None),
        "shadow_intensity": (Annotated[int, Field(ge=0, le=100)] | None, None),
        "sunlight_intensity": (Annotated[int, Field(ge=0, le=100)] | None, None),
        "sun_date": (str | None, None),
        "sun_time": (str | None, None),
        "sun_azimuth_deg": (Number | None, None),
        "sun_altitude_deg": (Number | None, None),
        "ground_plane": (bool | None, None),
        "ground_plane_level": (Name | None, None),
        "background": (Literal["sky", "gradient"] | None, None),
        "background_colors": (Annotated[list[str], Field(min_length=3, max_length=3)] | None, None),
        "lighting_scheme": (
            Literal[
                "exterior-sun",
                "exterior-sun-and-artificial",
                "exterior-artificial",
                "interior-sun",
                "interior-sun-and-artificial",
                "interior-artificial",
            ]
            | None,
            None,
        ),
    },
    "create_level": {
        "name": (Name, ...),
        "elevation_mm": (Number, ...),
        "create_view": (bool, False),
    },
    "create_floor": {
        "points_mm": (Points, ...),
        "level": (Name, ...),
        "floor_type": (Name | None, None),
    },
    "create_grid": {
        "label": (Name, ...),
        "start_mm": (Point, ...),
        "end_mm": (Point, ...),
        "mid_mm": (Point | None, None),
    },
    "create_column": {
        "family": (Name, ...),
        "type_name": (Name | None, None),
        "level": (Name, ...),
        "x_mm": (Number, ...),
        "y_mm": (Number, ...),
        "top_level": (Name | None, None),
        "height_mm": (Number | None, None),
        "base_offset_mm": (Number, 0),
        "top_offset_mm": (Number, 0),
        "rotation_deg": (Number, 0),
    },
    "create_beam": {
        "family": (Name, ...),
        "type_name": (Name | None, None),
        "level": (Name, ...),
        "start_mm": (Point, ...),
        "end_mm": (Point, ...),
        "structural_usage": (Name | None, None),
        "z_offset_mm": (Number, 0),
    },
    "load_family_file": {
        "path": (Name, ...),
        "type_name": (Name | None, None),
        "overwrite_parameters": (bool, False),
    },
    "place_hosted_family": {
        "family": (Name, ...),
        "type_name": (Name | None, None),
        "x_mm": (Number, ...),
        "y_mm": (Number, ...),
        "host_element_id": (ElementId | None, None),
        "host_search_radius_mm": (Number, 2000),
        "level": (Name | None, None),
        "rotation_deg": (Number, 0),
        "sill_height_mm": (Number | None, None),
        "flip_facing": (bool | None, None),
    },
    "set_phase": {
        "element_ids": (ElementIds, ...),
        "created_phase": (str | None, None),
        "demolished_phase": (str | None, None),
    },
    "merge_phases": {
        "source_phase": (Name, ...),
        "target_phase": (Name, ...),
    },
    "reset_element_ids": {
        "element_ids": (ElementIds, ...),
    },
    "rebuild_model_ids": {
        "destination_path": (str, ...),
        "view": (str | None, None),
        "template_path": (str | None, None),
        "overwrite": (bool, False),
        "remove_template_levels": (bool, True),
        "seed": (int, 0),
        "duplicate_names": (Literal["override", "rename"], "override"),
        "copies": (int, 1),
    },
}

# Which step fields travel at the top level of the wire command. Everything else travels in the fork
# bag: the add-in reads a sparse bag, so an absent key leaves that input alone (adr/0005).
STEP_TOP_LEVEL: dict[str, tuple[str, ...]] = {
    "set_view_lighting": ("view",),
    "create_level": ("name",),
    "create_floor": ("points_mm", "level"),
    "create_grid": ("label",),
    "create_column": ("family", "type_name", "level", "x_mm", "y_mm", "rotation_deg"),
    "create_beam": ("family", "type_name", "level"),
    "load_family_file": (),
    "place_hosted_family": ("family", "type_name", "x_mm", "y_mm", "level", "rotation_deg"),
    "set_phase": ("element_ids",),
    "merge_phases": (),
    "reset_element_ids": ("element_ids",),
    "rebuild_model_ids": ("view",),
}
_TOP_LEVEL_NAMES = {"element_ids": "elementIds", "points_mm": "pointsMm", "label": "name"}


def step_models() -> dict[str, Any]:
    """Step models for revit_run_actions, one per fork action, keyed by the step's action name."""
    from pydantic import ConfigDict, create_model

    return {
        action: create_model(
            action,
            __config__=ConfigDict(extra="forbid"),
            **{**fields, "dry_run": (bool, False)},
        )
        for action, fields in STEP_FIELDS.items()
    }


def check_step(action: str, args: dict[str, Any], refuse) -> None:
    """The same refusals the tool of this name makes, for the same reasons."""
    if action == "set_view_lighting":
        # The view names what to change, so it is not one of the settings being changed.
        settings = {
            _camel(key): value for key, value in args.items() if key not in ("view", "dry_run")
        }
        _check_lighting(settings, refuse)
    elif action == "create_floor":
        _check_floor_points(args["points_mm"], refuse)
    elif action == "create_grid":
        _check_grid_points(args["start_mm"], args["end_mm"], args["mid_mm"], refuse)
    elif action == "create_column":
        _check_column(args["height_mm"], refuse)
    elif action == "create_beam":
        _check_beam(args["start_mm"], args["end_mm"], refuse)
    elif action == "load_family_file":
        _check_family_path(args["path"], refuse)
    elif action == "place_hosted_family":
        _check_hosted(args["host_search_radius_mm"], args["rotation_deg"], refuse)
    elif action == "set_phase":
        _check_phase_assignment(args["created_phase"], args["demolished_phase"], refuse)
    elif action == "merge_phases":
        _check_phases_differ(args["source_phase"], args["target_phase"], refuse)


def step_payload(action: str, args: dict[str, Any]) -> dict[str, Any] | None:
    """The wire payload of one fork step, or None when the action is not a fork action."""
    top_level = STEP_TOP_LEVEL.get(action)
    if top_level is None:
        return None
    payload: dict[str, Any] = {"command": action.replace("_", "-")}
    fork: dict[str, Any] = {}
    for key, value in args.items():
        if key == "dry_run":
            payload["dryRun"] = value
        elif key in top_level:
            payload[_TOP_LEVEL_NAMES.get(key, _camel(key))] = value
        elif value is not None:
            fork[_camel(key)] = value
    if action == "rebuild_model_ids":
        # An empty view is the add-in's "the default 3D view", the same meaning the tool gives null.
        payload["view"] = payload.get("view") or ""
    if fork:
        payload["fork"] = fork
    return payload


def register_fork_actions(mcp, send) -> None:
    """Registers the fork's extra tools onto the shared MCP server.

    Every action goes through ``send`` so the policy gate, the address resolution and the transport
    stay upstream's. The element id register reads instead of changing, so it lives in
    ``register_fork_reads`` beside the other reads.
    """

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
        """Set a view's lighting: shadows, sun position, ground plane, background and lighting scheme.

        View-specific sun and shadow settings; a view that shares them passes the change on.
        Sun angles come as a pair, and gradient colors need the gradient background.
        dry_run returns the same verification block without changing the model."""
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
            "backgroundColors": background_colors,
            "lightingScheme": lighting_scheme,
        }
        _check_lighting(settings, ToolError)
        # Only what the caller passed travels: the add-in reads a sparse bag, so an absent key means
        # "leave this setting alone" rather than "set it to null" (adr/0005).
        fork = {name: value for name, value in settings.items() if value is not None}
        return await send(
            "set-view-lighting", view=view, fork=fork, dryRun=dry_run, document=document
        )

    @mcp.tool(
        title="Create Level",
        annotations=ToolAnnotations(
            title="Create Level",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_create_level(
        name: Name,
        elevation_mm: Number,
        create_view: bool = False,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Create a level at an elevation, optionally with its floor plan.

        A level whose name already exists is refused. dry_run returns the same verification block
        without changing the model."""
        return await send(
            "create-level",
            name=name,
            fork={"elevationMm": elevation_mm, "createView": create_view},
            dryRun=dry_run,
            document=document,
        )

    @mcp.tool(
        title="Create Floor",
        annotations=ToolAnnotations(
            title="Create Floor",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_create_floor(
        points_mm: Annotated[list[Point], Field(min_length=3)],
        level: Name,
        floor_type: Name | None = None,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Create a floor from a closed boundary on a level.

        `points_mm` is the polygon, three vertices or more, each [x, y] in millimetres; consecutive
        duplicates are refused. dry_run returns the same verification block without changing the model."""
        _check_floor_points(points_mm, ToolError)
        fork = {} if floor_type is None else {"floorType": floor_type}
        return await send(
            "create-floor",
            pointsMm=[list(point) for point in points_mm],
            level=level,
            fork=fork,
            dryRun=dry_run,
            document=document,
        )

    @mcp.tool(
        title="Create Grid",
        annotations=ToolAnnotations(
            title="Create Grid",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_create_grid(
        label: Name,
        start_mm: Point,
        end_mm: Point,
        mid_mm: Point | None = None,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Create a grid line: straight from `start_mm` to `end_mm`, or a three-point arc through `mid_mm`.

        `label` names the grid (Grid.Name); a grid whose name already exists is refused.
        Points are [x, y] in millimetres on the horizontal plane. dry_run returns the same
        verification block without changing the model."""
        _check_grid_points(start_mm, end_mm, mid_mm, ToolError)
        fork: dict[str, Any] = {
            "startMm": list(start_mm),
            "endMm": list(end_mm),
        }
        if mid_mm is not None:
            fork["midMm"] = list(mid_mm)
        return await send(
            "create-grid",
            name=label,
            fork=fork,
            dryRun=dry_run,
            document=document,
        )

    @mcp.tool(
        title="Load Family File",
        annotations=ToolAnnotations(
            title="Load Family File",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=True,
        ),
    )
    @with_client_identity
    async def revit_load_family_file(
        path: Name,
        type_name: Name | None = None,
        overwrite_parameters: bool = False,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Load one family file from the workstation: the whole family, or the single type `type_name`.

        The load always carries the family load options, so it never waits on Revit's own dialog.
        An existing family is reused, and its parameter values are left alone unless
        `overwrite_parameters` is true. The response reports `state` ("new" or "existing") and every
        type the family now offers. A path that does not exist is refused with the closest filenames
        beside it. dry_run returns the same verification block without changing the model."""
        _check_family_path(path, ToolError)
        fork: dict[str, Any] = {"path": path}
        if type_name is not None:
            fork["typeName"] = type_name
        if overwrite_parameters:
            fork["overwriteParameters"] = True
        return await send(
            "load-family-file",
            fork=fork,
            dryRun=dry_run,
            document=document,
        )

    @mcp.tool(
        title="Place Hosted Family",
        annotations=ToolAnnotations(
            title="Place Hosted Family",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_place_hosted_family(
        family: Name,
        x_mm: Number,
        y_mm: Number,
        type_name: Name | None = None,
        host_element_id: ElementId | None = None,
        host_search_radius_mm: Number = 2000,
        level: Name | None = None,
        rotation_deg: Number = 0,
        sill_height_mm: Number | None = None,
        flip_facing: bool | None = None,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Place one door, window or other one-level hosted family of `family` at `x_mm`, `y_mm`.

        The host is either the wall named by `host_element_id`, or the nearest wall of the placement
        level whose location line passes within `host_search_radius_mm` of the point; `level` defaults
        to the level whose elevation is closest to the point. A missing host, a distance over the
        radius or two equally near walls are refused with the candidates, so the caller can name one.
        The response reports `fork.hostResolution` ({mode, hostId, distanceMm}), which is why a dry
        run already shows the wall the family would hang on. `sill_height_mm` writes the family's own
        INSTANCE_SILL_HEIGHT_PARAM and `flip_facing` calls flipFacing(). `rotation_deg` must be 0: a
        hosted instance takes its orientation from its host wall, so use `flip_facing` to turn it
        around. Families that are not one-level hosted are refused: revit_place_family places those,
        and it is the one that rotates. Nothing is attached to the host, because a door or a window
        has no attachment target. dry_run returns the same verification block without changing the
        model."""
        _check_hosted(host_search_radius_mm, rotation_deg, ToolError)
        fork: dict[str, Any] = {"hostSearchRadiusMm": host_search_radius_mm}
        if host_element_id is not None:
            fork["hostElementId"] = host_element_id
        if sill_height_mm is not None:
            fork["sillHeightMm"] = sill_height_mm
        if flip_facing is not None:
            fork["flipFacing"] = flip_facing
        return await send(
            "place-hosted-family",
            family=family,
            typeName=type_name,
            level=level,
            xMm=x_mm,
            yMm=y_mm,
            rotationDeg=rotation_deg,
            fork=fork,
            dryRun=dry_run,
            document=document,
        )

    @mcp.tool(
        title="Create Column",
        annotations=ToolAnnotations(
            title="Create Column",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_create_column(
        family: Name,
        level: Name,
        x_mm: Number,
        y_mm: Number,
        type_name: Name | None = None,
        top_level: Name | None = None,
        height_mm: Number | None = None,
        base_offset_mm: Number = 0,
        top_offset_mm: Number = 0,
        rotation_deg: Number = 0,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Place one structural column of `family` (optionally `type_name`) at `x_mm`, `y_mm` on `level`.

        The top is either `top_level` or `height_mm` above the base (3000 mm when neither is given).
        Base and top levels and both offsets are written by the tool itself, because they are
        ElementId-valued parameters that revit_set_parameter refuses on purpose. The column is not
        attached to anything: no attachment is attempted. dry_run returns the same verification
        block without changing the model."""
        _check_column(height_mm, ToolError)
        fork: dict[str, Any] = {
            "baseOffsetMm": base_offset_mm,
            "topOffsetMm": top_offset_mm,
        }
        if top_level is not None:
            fork["topLevel"] = top_level
        else:
            fork["heightMm"] = height_mm if height_mm is not None else 3000
        return await send(
            "create-column",
            family=family,
            typeName=type_name,
            level=level,
            xMm=x_mm,
            yMm=y_mm,
            rotationDeg=rotation_deg,
            fork=fork,
            dryRun=dry_run,
            document=document,
        )

    @mcp.tool(
        title="Create Beam",
        annotations=ToolAnnotations(
            title="Create Beam",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_create_beam(
        family: Name,
        level: Name,
        start_mm: Point,
        end_mm: Point,
        type_name: Name | None = None,
        structural_usage: Name | None = None,
        z_offset_mm: Number = 0,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Place one structural beam of `family` (optionally `type_name`) along the axis `start_mm`-`end_mm`.

        `level` is the reference level of the framing, and the two axis points are [x, y] in
        millimetres. The placement uses the curve-and-level overload, so the level and the axis are
        both given explicitly; the axis is not snapped, because Revit has no snapping API and
        SetEndReference only acts on an end the model already joined. `structural_usage` writes
        FamilyInstance.StructuralUsage. `z_offset_mm` is the vertical offset above the reference
        level: the tool writes it through the elevation parameters that carry it, and only a write that
        lifts the bounding box counts, because a family can take the value and keep the beam on its
        level; the instance moves instead when no parameter lifts it, and the call fails when neither
        route works, so a refused offset never passes as a beam placed on the level. The read-back names
        the parameter holding the offset or leaves it out when the geometry carries the shift. dry_run
        returns the same verification block without changing the model."""
        _check_beam(start_mm, end_mm, ToolError)
        fork: dict[str, Any] = {
            "startMm": list(start_mm),
            "endMm": list(end_mm),
            "zOffsetMm": z_offset_mm,
        }
        if structural_usage is not None:
            fork["structuralUsage"] = structural_usage
        return await send(
            "create-beam",
            family=family,
            typeName=type_name,
            level=level,
            fork=fork,
            dryRun=dry_run,
            document=document,
        )

    @mcp.tool(
        title="Set Phase",
        annotations=ToolAnnotations(
            title="Set Phase",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=True,
        ),
    )
    @with_client_identity
    async def revit_set_phase(
        element_ids: Annotated[list[ElementId], Field(min_length=1)],
        created_phase: str | None = None,
        demolished_phase: str | None = None,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Set the creation and demolition phase of elements.

        An empty string clears a phase and null leaves it alone; at least one must be given.
        dry_run returns the same verification block without changing the model."""
        _check_phase_assignment(created_phase, demolished_phase, ToolError)
        fork = {
            name: value
            for name, value in (
                ("createdPhase", created_phase),
                ("demolishedPhase", demolished_phase),
            )
            if value is not None
        }
        return await send(
            "set-phase",
            elementIds=element_ids,
            fork=fork,
            dryRun=dry_run,
            document=document,
        )

    @mcp.tool(
        title="Merge Phases",
        annotations=ToolAnnotations(
            title="Merge Phases",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_merge_phases(
        source_phase: Name,
        target_phase: Name,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Merge one phase into another and delete the emptied phase.

        Reports how many elements moved each way and how many references remain to the source.
        dry_run returns the same verification block without changing the model."""
        _check_phases_differ(source_phase, target_phase, ToolError)
        return await send(
            "merge-phases",
            fork={"sourcePhase": source_phase, "targetPhase": target_phase},
            dryRun=dry_run,
            document=document,
        )

    @mcp.tool(
        title="Reset Element Ids",
        annotations=ToolAnnotations(
            title="Reset Element Ids",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_reset_element_ids(
        element_ids: Annotated[list[ElementId], Field(min_length=1)],
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Give elements new element IDs by copying each one over its original.

        The API cannot assign an element ID, so every element is copied, checked and then replaces
        its original. Elements that cannot be replaced are refused by name, and a real run is
        refused when any element in the selection is. dry_run returns the same block without keeping
        the changes."""
        return await send(
            "reset-element-ids",
            elementIds=element_ids,
            dryRun=dry_run,
            document=document,
        )

    @mcp.tool(
        title="Rebuild Model Ids",
        annotations=ToolAnnotations(
            title="Rebuild Model Ids",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_rebuild_model_ids(
        destination_path: str,
        view: str | None = None,
        template_path: str | None = None,
        overwrite: bool = False,
        remove_template_levels: bool = True,
        seed: int = 0,
        duplicate_names: Literal["override", "rename"] = "override",
        copies: int = 1,
        dry_run: bool = False,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Rebuild the model into a new document so every element gets a new element ID.

        `destination_path` is the new model, with {n} replaced by the copy number when `copies`
        exceeds one. Reports the old to new pairing, the per-file results and the category counts.
        dry_run reports the plan without writing files."""
        fork = {
            name: value
            for name, value in (
                ("destinationPath", destination_path),
                ("templatePath", template_path),
                ("overwrite", overwrite),
                ("removeTemplateLevels", remove_template_levels),
                ("seed", seed),
                ("duplicateNames", duplicate_names),
                ("copies", copies),
            )
            if value is not None
        }
        return await send(
            "rebuild-model-ids",
            view="" if view is None else view,
            fork=fork,
            dryRun=dry_run,
            document=document,
        )


def register_fork_reads(mcp, execute) -> None:
    """Registers the fork's extra read tools onto the shared MCP server.

    The element id register reads the model instead of changing it, so it goes through ``execute``,
    the dispatcher every upstream read tool uses, and stays usable on a read-only workstation.
    """

    @mcp.tool(
        title="Export Element Ids",
        annotations=ToolAnnotations(
            title="Export Element Ids",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=False,
        ),
    )
    @with_client_identity
    async def revit_export_element_ids(
        fields: list[str] | None = None,
        path: str | None = None,
        timeout_seconds: Annotated[int, Field(strict=True, ge=1, le=600)] = DEFAULT_TIMEOUT_SECONDS,
        document: str | None = None,
    ) -> dict[str, Any]:
        """Write the element identifier register of the drawn components to a workbook, read-only.

        `fields` picks the columns and `path` names the file, which must not already exist; without
        one the workbook goes to Documents/RevitModelMcp/Exports with a timestamp. Non-component
        categories are reported under skippedCategories and the list is capped at 50,000 rows.
        The workbook is written on the Revit workstation; nothing is downloaded."""
        payload: dict[str, Any] = {"command": "export-element-ids"}
        if fields:
            payload["fields"] = fields
        if path:
            # The add-in reads the destination as saveTo, the name the read contract already uses.
            payload["saveTo"] = path
        return await execute(Job("export-element-ids", payload), timeout_seconds, document)
