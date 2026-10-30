"""Tests for the structural input-schema diff used on twin tool pages.

The pages must never carry a hand-written difference list; the hint is computed from the two
registry schemas so it cannot drift. These tests pin the change kinds the ticket calls out:
presence, required, type, default and constraints such as enum and minimum.
"""

import unittest

import contract_diff


def schema(properties, required=()):
    return {
        "type": "object",
        "properties": properties,
        "required": list(required),
    }


class DiffDetectionTests(unittest.TestCase):
    def test_identical_schemas_have_no_changes(self):
        s = schema({"view": {"type": "string"}}, ["view"])
        self.assertEqual(contract_diff.diff_schemas(s, s), [])

    def test_a_parameter_only_in_one_catalog_is_reported(self):
        release = schema({"save_to": {"type": "string"}})
        integration = schema({"output_path": {"type": "string"}})
        changes = contract_diff.diff_schemas(release, integration)
        kinds = {(c["kind"], c["param"]) for c in changes}
        self.assertIn(("only_in_release", "save_to"), kinds)
        self.assertIn(("only_in_integration", "output_path"), kinds)

    def test_a_required_change_is_reported(self):
        release = schema({"view": {"type": "string"}}, [])
        integration = schema({"view": {"type": "string"}}, ["view"])
        changes = contract_diff.diff_schemas(release, integration)
        required = [c for c in changes if c["kind"] == "required"]
        self.assertEqual(required[0]["param"], "view")
        self.assertFalse(required[0]["release"])
        self.assertTrue(required[0]["integration"])

    def test_a_type_change_is_reported(self):
        release = schema({"pixel_size": {"type": "integer"}})
        integration = schema({"pixel_size": {"type": "string"}})
        changes = contract_diff.diff_schemas(release, integration)
        types = [c for c in changes if c["kind"] == "type"]
        self.assertEqual(types[0]["release"], "integer")
        self.assertEqual(types[0]["integration"], "string")

    def test_a_default_change_is_reported(self):
        release = schema({"pixel_size": {"type": "integer", "default": 1600}})
        integration = schema({"pixel_size": {"type": "integer", "default": 32}})
        changes = contract_diff.diff_schemas(release, integration)
        defaults = [c for c in changes if c["kind"] == "default"]
        self.assertEqual(len(defaults), 1)

    def test_a_missing_default_is_a_change(self):
        release = schema({"x": {"type": "string"}})
        integration = schema({"x": {"type": "string", "default": "a"}})
        changes = contract_diff.diff_schemas(release, integration)
        self.assertIn("default", [c["kind"] for c in changes])

    def test_an_enum_change_is_reported(self):
        release = schema({"mode": {"type": "string", "enum": ["a", "b"]}})
        integration = schema({"mode": {"type": "string", "enum": ["a", "b", "c"]}})
        changes = contract_diff.diff_schemas(release, integration)
        enum = [c for c in changes if c["kind"] == "constraint" and c["key"] == "enum"]
        self.assertEqual(len(enum), 1)

    def test_a_minimum_change_is_reported(self):
        release = schema({"pixel_size": {"type": "integer", "minimum": 1}})
        integration = schema({"pixel_size": {"type": "integer", "minimum": 32}})
        changes = contract_diff.diff_schemas(release, integration)
        keys = [c["key"] for c in changes if c["kind"] == "constraint"]
        self.assertIn("minimum", keys)

    def test_anyof_types_compare_by_their_member_types(self):
        release = schema({"d": {"anyOf": [{"type": "string"}, {"type": "null"}]}})
        integration = schema({"d": {"anyOf": [{"type": "string"}, {"type": "null"}]}})
        self.assertEqual(contract_diff.diff_schemas(release, integration), [])


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.release = schema(
            {
                "save_to": {"type": "string"},
                "pixel_size": {"type": "integer", "minimum": 1},
            }
        )
        self.integration = schema(
            {
                "output_path": {"type": "string"},
                "pixel_size": {"type": "integer", "minimum": 32},
            }
        )
        self.changes = contract_diff.diff_schemas(self.release, self.integration)

    def test_chinese_render_names_every_changed_parameter(self):
        text = "\n".join(contract_diff.render_changes(self.changes, "zh"))
        for token in ("save_to", "output_path", "pixel_size"):
            self.assertIn(token, text)

    def test_english_render_names_every_changed_parameter(self):
        text = "\n".join(contract_diff.render_changes(self.changes, "en"))
        for token in ("save_to", "output_path", "pixel_size"):
            self.assertIn(token, text)

    def test_render_is_stable(self):
        first = contract_diff.render_changes(self.changes, "zh")
        second = contract_diff.render_changes(
            contract_diff.diff_schemas(self.release, self.integration), "zh"
        )
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
