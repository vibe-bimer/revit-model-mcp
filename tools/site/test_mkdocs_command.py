"""Tests for the single mkdocs lookup shared by the publisher and the dual-build checker."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import mkdocs_command


class BuilderCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.home = self.base / "home"
        self.home.mkdir()
        # An isolated HOME without a ~/.venv-docs so the developer's own install cannot leak in.
        patcher = mock.patch("pathlib.Path.home", return_value=self.home)
        patcher.start()
        self.addCleanup(patcher.stop)

    def _secrets(self):
        return mock.patch.dict(os.environ, {"MKDOCS": ""}, clear=False)

    def test_an_explicit_mkdocs_with_a_space_stays_one_argument(self):
        with (
            self._secrets(),
            mock.patch.dict(os.environ, {"MKDOCS": '"/tmp/docs env/bin/mkdocs"'}),
        ):
            self.assertEqual(
                mkdocs_command.builder_command(self.repo),
                ["/tmp/docs env/bin/mkdocs"],
            )

    def test_an_explicit_mkdocs_keeps_extra_arguments(self):
        with mock.patch.dict(os.environ, {"MKDOCS": "python -m mkdocs"}):
            self.assertEqual(
                mkdocs_command.builder_command(self.repo), ["python", "-m", "mkdocs"]
            )

    def test_the_repo_virtualenv_is_preferred(self):
        venv = self.repo / ".venv-docs" / "bin" / "mkdocs"
        venv.parent.mkdir(parents=True)
        venv.write_text("#!/bin/sh\n", encoding="utf-8")
        with self._secrets():
            self.assertEqual(mkdocs_command.builder_command(self.repo), [str(venv)])

    def test_a_mkdocs_on_path_is_used_when_no_venv_exists(self):
        with (
            self._secrets(),
            mock.patch("mkdocs_command.shutil.which", return_value="/usr/bin/mkdocs"),
        ):
            self.assertEqual(
                mkdocs_command.builder_command(self.repo), ["/usr/bin/mkdocs"]
            )

    def test_uv_installs_from_the_requirements_when_nothing_else_exists(self):
        source = self.base / "export"
        (source / "docs").mkdir(parents=True)
        requirements = source / "docs" / "requirements.txt"
        requirements.write_text("mkdocs\n", encoding="utf-8")

        def which(name):
            return "/usr/bin/uv" if name == "uv" else None

        with (
            self._secrets(),
            mock.patch("mkdocs_command.shutil.which", side_effect=which),
        ):
            self.assertEqual(
                mkdocs_command.builder_command(self.repo, source),
                ["uv", "run", "--with-requirements", str(requirements), "mkdocs"],
            )

    def test_no_mkdocs_anywhere_raises(self):
        with (
            self._secrets(),
            mock.patch("mkdocs_command.shutil.which", return_value=None),
            self.assertRaises(mkdocs_command.BuilderNotFound),
        ):
            mkdocs_command.builder_command(self.repo)

    def test_uv_is_not_offered_without_a_source_requirements_file(self):
        def which(name):
            return "/usr/bin/uv" if name == "uv" else None

        with (
            self._secrets(),
            mock.patch("mkdocs_command.shutil.which", side_effect=which),
            self.assertRaises(mkdocs_command.BuilderNotFound),
        ):
            mkdocs_command.builder_command(self.repo)


if __name__ == "__main__":
    unittest.main()
