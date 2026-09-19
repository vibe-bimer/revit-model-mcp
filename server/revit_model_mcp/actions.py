from __future__ import annotations

import os
from typing import Annotated, Any, Literal

from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, create_model, model_validator

from revit_model_mcp.revit_channel import (
    DEFAULT_PICKUP_TIMEOUT_SECONDS,
    DEFAULT_TIMEOUT_SECONDS,
    ReadJob,
    RevitChannelError,
)

ElementId = Annotated[int, Field(strict=True, gt=0, le=9223372036854775807)]
ElementIds = list[ElementId]
NonEmptyIds = Annotated[ElementIds, Field(min_length=1)]
Number = Annotated[float, Field(allow_inf_nan=False)]
PositiveLength = Annotated[float, Field(gt=0, allow_inf_nan=False)]
Name = Annotated[str, Field(min_length=1, pattern=r"\S")]
Point = Annotated[list[Number], Field(min_length=2, max_length=2)]
Document = Annotated[
    str | None,
    Field(
        validation_alias=AliasChoices("document", "targetDocument"),
        description="Case-insensitive substring of the target open document's title or file name. Required to disambiguate when the Revit process has more than one document open; omit only when a single document is open (the active document is used). An unknown or ambiguous reference is rejected before any change.",
    ),
]


_BATCH_FIELDS = {
    "select": {"element_ids": (ElementIds, ...)},
    "isolate": {"element_ids": (ElementIds, ...), "reset": (bool, False)},
    "move": {
        "element_ids": (NonEmptyIds, ...),
        "dx_mm": (Number, ...),
        "dy_mm": (Number, ...),
        "dz_mm": (Number, 0),
    },
    "place_family": {
        "family": (Name, ...),
        "type_name": (Name | None, ...),
        "x_mm": (Number, ...),
        "y_mm": (Number, ...),
        "level": (Name, ...),
        "rotation_deg": (Number, 0),
    },
    "create_wall": {
        "start_mm": (Point, ...),
        "end_mm": (Point, ...),
        "level": (Name, ...),
        "wall_type": (Name | None, ...),
        "height_mm": (PositiveLength, 3000),
    },
    "create_floor": {
        "points_mm": (Annotated[list[Point], Field(min_length=3)], ...),
        "level": (Name, ...),
        "floor_type": (Name | None, ...),
    },
    "set_phase": {
        "element_ids": (NonEmptyIds, ...),
        "created_phase": (str | None, ...),
        "demolished_phase": (str | None, ...),
    },
    "set_parameter": {
        "element_id": (ElementId, ...),
        "parameter": (Name, ...),
        "value": (str, ...),
    },
    "delete": {"element_ids": (NonEmptyIds, ...)},
}
for _action in (
    "move",
    "place_family",
    "create_wall",
    "create_floor",
    "set_phase",
    "set_parameter",
    "delete",
):
    _BATCH_FIELDS[_action]["dry_run"] = (bool, False)
_BATCH_MODELS = {
    action: create_model(action, __config__=ConfigDict(extra="forbid"), **fields)
    for action, fields in _BATCH_FIELDS.items()
}


class BatchStep(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal[
        "move",
        "place_family",
        "create_wall",
        "create_floor",
        "set_phase",
        "set_parameter",
        "delete",
        "select",
        "isolate",
    ]
    args: dict

    @model_validator(mode="after")
    def validate_args(self):
        self.args = _BATCH_MODELS[self.action].model_validate(self.args).model_dump()
        if self.action == "isolate" and not self.args["reset"] and not self.args["element_ids"]:
            raise ValueError("element_ids must not be empty unless reset is true.")
        if self.action == "create_wall" and self.args["start_mm"] == self.args["end_mm"]:
            raise ValueError("Wall endpoints must differ.")
        if self.action == "create_floor":
            points = self.args["points_mm"]
            if any(
                points[index] == points[(index + 1) % len(points)] for index in range(len(points))
            ):
                raise ValueError("Floor boundary points must not repeat consecutively.")
        if (
            self.action == "set_phase"
            and self.args["created_phase"] is None
            and self.args["demolished_phase"] is None
        ):
            raise ValueError("At least one of created_phase or demolished_phase is required.")
        return self

    def payload(self) -> dict:
        def camel(key):
            first, *rest = key.split("_")
            return first + "".join(part.title() for part in rest)

        return {
            "command": self.action.replace("_", "-"),
            **{camel(key): value for key, value in self.args.items()},
        }


def env_flag(name: str, default: bool = False) -> bool:
    """Read a boolean environment setting; reject unrecognized values."""
    value = os.environ.get(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be 1/0, true/false, yes/no or on/off.")


def millimeters_to_feet(value: float) -> float:
    """Convert a finite millimetre length to Revit internal feet for client calculations."""
    import math

    if not math.isfinite(value):
        raise ValueError("Length must be finite.")
    return value / 304.8


def register_actions(mcp, execute, host_provider) -> None:
    if not env_flag("REVIT_MCP_ALLOW_WRITE", False):
        return

    async def send(command: str, *, document: str | None = None, **payload) -> dict[str, Any]:
        try:
            instances = await host_provider().list_revit_instances()
        except RevitChannelError as error:
            raise ToolError(str(error)) from error
        if len(instances) != 1:
            raise ToolError("Actions require exactly one running Revit instance.")
        if document is not None:
            payload["targetDocument"] = document
        job = ReadJob(
            command,
            {
                "command": command,
                **payload,
                "targetProcessId": instances[0]["processId"],
            },
        )
        return await execute(job, DEFAULT_TIMEOUT_SECONDS, DEFAULT_PICKUP_TIMEOUT_SECONDS, None)

    def action(function):
        title = {
            "revit_select": "Select Elements",
            "revit_show": "Show Elements",
            "revit_isolate": "Isolate Elements",
            "revit_move": "Move Elements",
            "revit_place_family": "Place Family",
            "revit_create_wall": "Create Wall",
            "revit_create_floor": "Create Floor",
            "revit_set_phase": "Set Element Phases",
            "revit_merge_phases": "Merge Phases",
            "revit_set_parameter": "Set Parameter",
            "revit_delete": "Delete Elements",
            "revit_batch": "Run Action Batch",
        }[function.__name__]
        return mcp.tool(
            title=title,
            annotations=ToolAnnotations(
                title=title,
                readOnlyHint=False,
                destructiveHint=function.__name__
                not in {"revit_select", "revit_show", "revit_isolate"},
                idempotentHint=function.__name__
                in {
                    "revit_select",
                    "revit_show",
                    "revit_isolate",
                    "revit_set_parameter",
                    "revit_set_phase",
                },
            ),
        )(function)

    @action
    async def revit_select(element_ids: ElementIds, document: Document = None) -> dict[str, Any]:
        """Select element IDs for inspection in Revit; an empty list clears selection; IDs are unitless.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        return await send("select", elementIds=element_ids, document=document)

    @action
    async def revit_show(
        element_ids: NonEmptyIds, select: bool = True, document: Document = None
    ) -> dict[str, Any]:
        """Show elements, optionally selecting them; open a level plan or 3D view when needed. Returns activeView, viewOpened and dialogsSuppressed; IDs are unitless.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        return await send("show", elementIds=element_ids, select=select, document=document)

    @action
    async def revit_isolate(
        element_ids: ElementIds, reset: bool = False, document: Document = None
    ) -> dict[str, Any]:
        """Temporarily isolate IDs for visual review in the active view, or reset with an empty list; IDs are unitless.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        if not reset and not element_ids:
            raise ToolError("element_ids must not be empty unless reset is true.")
        return await send("isolate", elementIds=element_ids, reset=reset, document=document)

    @action
    async def revit_move(
        element_ids: NonEmptyIds,
        dx_mm: Number,
        dy_mm: Number,
        dz_mm: Number = 0,
        dry_run: bool = False,
        document: Document = None,
    ) -> dict[str, Any]:
        """Move elements when adjusting their position; dx_mm, dy_mm and dz_mm are offsets in millimetres on model axes.
        dry_run executes and rolls back, returning the same verification block without changing the model.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        return await send(
            "move",
            elementIds=element_ids,
            dxMm=dx_mm,
            dyMm=dy_mm,
            dzMm=dz_mm,
            dryRun=dry_run,
            document=document,
        )

    @action
    async def revit_place_family(
        family: Name,
        type_name: Name | None,
        x_mm: Number,
        y_mm: Number,
        level: Name,
        rotation_deg: Number = 0,
        dry_run: bool = False,
        document: Document = None,
    ) -> dict[str, Any]:
        """Place a loaded unhosted family on a named level for layout.

        family accepts a family name or Family: Type, case-insensitively.
        null type_name uses the embedded type or the first type. Conflicting types
        are rejected. Missing families return similar names with categories.
        Model XY is in millimetres and Z rotation in degrees.
        Use roomCenterMm when placing something inside a room.

        dry_run executes and rolls back, returning the same verification block without changing the model.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        return await send(
            "place-family",
            family=family,
            typeName=type_name,
            xMm=x_mm,
            yMm=y_mm,
            level=level,
            rotationDeg=rotation_deg,
            dryRun=dry_run,
            document=document,
        )

    @action
    async def revit_create_wall(
        start_mm: Point,
        end_mm: Point,
        level: Name,
        wall_type: Name | None,
        height_mm: PositiveLength = 3000,
        dry_run: bool = False,
        document: Document = None,
    ) -> dict[str, Any]:
        """Create a straight wall for layout on a named level; model XY endpoints and height are millimetres; null wall_type chooses the first basic type.
        dry_run executes and rolls back, returning the same verification block without changing the model.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        if start_mm == end_mm:
            raise ToolError("Wall endpoints must differ.")
        return await send(
            "create-wall",
            startMm=start_mm,
            endMm=end_mm,
            level=level,
            wallType=wall_type,
            heightMm=height_mm,
            dryRun=dry_run,
            document=document,
        )

    @action
    async def revit_create_floor(
        points_mm: Annotated[list[Point], Field(min_length=3)],
        level: Name,
        floor_type: Name | None,
        dry_run: bool = False,
        document: Document = None,
    ) -> dict[str, Any]:
        """Create a floor from a closed boundary for layout on a named level.
        points_mm are model XY polygon vertices in millimetres (at least 3; the
        boundary closes automatically); null floor_type chooses the first floor type.
        dry_run executes and rolls back, returning the same verification block without changing the model.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        if any(
            points_mm[index] == points_mm[(index + 1) % len(points_mm)]
            for index in range(len(points_mm))
        ):
            raise ToolError("Floor boundary points must not repeat consecutively.")
        return await send(
            "create-floor",
            pointsMm=points_mm,
            level=level,
            floorType=floor_type,
            dryRun=dry_run,
            document=document,
        )

    @action
    async def revit_set_phase(
        element_ids: NonEmptyIds,
        created_phase: str | None,
        demolished_phase: str | None,
        dry_run: bool = False,
        document: Document = None,
    ) -> dict[str, Any]:
        """Assign the created or demolished project phase of elements by exact phase name.

        Each phase argument is a phase name from revit_list_catalog(section="phases"),
        an empty string to clear that assignment, or null to leave it unchanged;
        at least one argument must be non-null. Creation APIs cannot add phases;
        create new phases in the Revit UI first. Example: demolished_phase="现有"
        marks elements demolished in that phase, demolished_phase="" clears it.
        dry_run executes and rolls back, returning the same verification block without changing the model.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        if created_phase is None and demolished_phase is None:
            raise ToolError("At least one of created_phase or demolished_phase is required.")
        for label, value in (
            ("created_phase", created_phase),
            ("demolished_phase", demolished_phase),
        ):
            if value is not None and value != "" and not value.strip():
                raise ToolError(f"{label} must be a phase name, an empty string to clear, or null.")
        return await send(
            "set-phase",
            elementIds=element_ids,
            createdPhase=created_phase,
            demolishedPhase=demolished_phase,
            dryRun=dry_run,
            document=document,
        )

    @action
    async def revit_merge_phases(
        source_phase: Name,
        target_phase: Name,
        dry_run: bool = False,
        document: Document = None,
    ) -> dict[str, Any]:
        """Merge one project phase into another by moving every element reference.

        Elements created in the source phase are reassigned to the target phase,
        demolitions recorded in the source phase move to the target, then the empty
        source phase is deleted. Revit may refuse the deletion when views or other
        objects still reference it; the response then reports reassigned counts with
        sourceDeleted:false. Phases themselves are never created or renamed here.
        dry_run executes and rolls back, returning the same verification block without changing the model.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        if source_phase == target_phase:
            raise ToolError("source_phase and target_phase must differ.")
        return await send(
            "merge-phases",
            sourcePhase=source_phase,
            targetPhase=target_phase,
            dryRun=dry_run,
            document=document,
        )

    @action
    async def revit_set_parameter(
        element_id: ElementId,
        parameter: Name,
        value: str,
        dry_run: bool = False,
        document: Document = None,
    ) -> dict[str, Any]:
        """Set a named instance parameter, falling back to its shared type; use for edits, with length in mm, area in m2 and other doubles in internal units.
        dry_run executes and rolls back, returning the same verification block without changing the model.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        return await send(
            "set-parameter",
            elementId=element_id,
            parameter=parameter,
            value=value,
            dryRun=dry_run,
            document=document,
        )

    @action
    async def revit_delete(
        element_ids: NonEmptyIds, dry_run: bool = False, document: Document = None
    ) -> dict[str, Any]:
        """Delete elements and their Revit dependencies when removal is intended; IDs are unitless and the returned count includes dependents.
        dry_run executes and rolls back, returning the same verification block without changing the model.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        return await send("delete", elementIds=element_ids, dryRun=dry_run, document=document)

    @action
    async def revit_batch(
        steps: Annotated[list[BatchStep], Field(min_length=1, max_length=50)],
        dry_run: bool = False,
        document: Document = None,
    ) -> dict[str, Any]:
        """Execute up to 50 actions with one undo step; roll back the batch on its first failure.

        dry_run executes and rolls back, returning the same verification block without changing the model.
        Pass `document` to address a specific open model when several are open; an unknown or ambiguous reference is rejected.
        """
        return await send(
            "batch", steps=[step.payload() for step in steps], dryRun=dry_run, document=document
        )
