#!/usr/bin/env python3
"""Structural diff between two tool input schemas.

Twin pages (a released tool and a same-named integration tool) must tell readers exactly how
the contracts differ. That hint is computed here from the registry inputSchema objects, so it
can never fall out of step with the contracts. The diff covers parameter presence, required,
type, default and constraints such as enum, minimum, maximum and length bounds.
"""

from __future__ import annotations

import json

# Constraint keywords compared when both catalogs declare the parameter.
CONSTRAINTS = (
    "enum",
    "minimum",
    "maximum",
    "exclusiveMinimum",
    "exclusiveMaximum",
    "minLength",
    "maxLength",
    "pattern",
    "minItems",
    "maxItems",
)

MISSING = object()


def _type_of(spec: dict) -> str:
    """A stable type string, folding anyOf members into a sorted union."""
    if "type" in spec:
        return str(spec["type"])
    members = spec.get("anyOf")
    if members:
        names = sorted({str(m.get("type", "any")) for m in members})
        return "|".join(names)
    return "any"


def _spec(schema: dict, name: str) -> dict:
    return (schema.get("properties") or {}).get(name) or {}


def _default(spec: dict):
    return spec.get("default", MISSING)


def _show(value) -> str:
    """Render a JSON value for the hint; distinguish an absent default from null."""
    if value is MISSING:
        return "—"
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return json.dumps(value)
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def diff_schemas(release_schema: dict, integration_schema: dict) -> list[dict]:
    """Return the ordered list of changes from the released to the integration contract."""
    release_props = release_schema.get("properties") or {}
    integration_props = integration_schema.get("properties") or {}
    names = sorted(set(release_props) | set(integration_props))
    release_required = set(release_schema.get("required") or [])
    integration_required = set(integration_schema.get("required") or [])

    changes: list[dict] = []
    for name in names:
        if name not in integration_props:
            changes.append({"kind": "only_in_release", "param": name})
            continue
        if name not in release_props:
            changes.append({"kind": "only_in_integration", "param": name})
            continue

        release_spec = _spec(release_schema, name)
        integration_spec = _spec(integration_schema, name)

        release_req = name in release_required
        integration_req = name in integration_required
        if release_req != integration_req:
            changes.append(
                {
                    "kind": "required",
                    "param": name,
                    "release": release_req,
                    "integration": integration_req,
                }
            )

        release_type = _type_of(release_spec)
        integration_type = _type_of(integration_spec)
        if release_type != integration_type:
            changes.append(
                {
                    "kind": "type",
                    "param": name,
                    "release": release_type,
                    "integration": integration_type,
                }
            )

        release_default = _default(release_spec)
        integration_default = _default(integration_spec)
        if _show(release_default) != _show(integration_default):
            changes.append(
                {
                    "kind": "default",
                    "param": name,
                    "release": _show(release_default),
                    "integration": _show(integration_default),
                }
            )

        for key in CONSTRAINTS:
            release_value = release_spec.get(key, MISSING)
            integration_value = integration_spec.get(key, MISSING)
            if _show(release_value) != _show(integration_value):
                changes.append(
                    {
                        "kind": "constraint",
                        "param": name,
                        "key": key,
                        "release": _show(release_value),
                        "integration": _show(integration_value),
                    }
                )
    return changes


_LABELS = {
    "zh": {
        "only_in_release": "仅发布版有参数 {param}",
        "only_in_integration": "仅集成分支有参数 {param}",
        "required": "参数 {param} 是否必填：发布版 {release} / 集成分支 {integration}",
        "type": "参数 {param} 类型：发布版 {release} / 集成分支 {integration}",
        "default": "参数 {param} 默认值：发布版 {release} / 集成分支 {integration}",
        "constraint": "参数 {param} 约束 {key}：发布版 {release} / 集成分支 {integration}",
        "yes": "是",
        "no": "否",
    },
    "en": {
        "only_in_release": "Parameter {param} exists only in the release",
        "only_in_integration": "Parameter {param} exists only on the integration branch",
        "required": "Parameter {param} required: release {release} / integration {integration}",
        "type": "Parameter {param} type: release {release} / integration {integration}",
        "default": "Parameter {param} default: release {release} / integration {integration}",
        "constraint": "Parameter {param} {key}: release {release} / integration {integration}",
        "yes": "yes",
        "no": "no",
    },
}


def render_changes(changes: list[dict], lang: str) -> list[str]:
    """Render each change as one stable line in the requested language."""
    labels = _LABELS.get(lang, _LABELS["en"])
    yes, no = labels["yes"], labels["no"]

    def flag(value: bool) -> str:
        return yes if value else no

    lines: list[str] = []
    for change in changes:
        kind = change["kind"]
        template = labels[kind]
        lines.append(
            template.format(
                param=change["param"],
                release=flag(change["release"])
                if kind == "required"
                else change.get("release", ""),
                integration=flag(change["integration"])
                if kind == "required"
                else change.get("integration", ""),
                key=change.get("key", ""),
            )
        )
    return lines


def changes_for(
    name: str, release_schemas: dict, integration_schemas: dict
) -> list[dict]:
    """Diff one tool when both catalogs carry the same name; empty when either is absent."""
    if name not in release_schemas or name not in integration_schemas:
        return []
    return diff_schemas(release_schemas[name], integration_schemas[name])
