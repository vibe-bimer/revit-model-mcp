"""The fork's own bounds are checked, not assumed: the budget gate and the base it measures against."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

BUILD = Path(__file__).resolve().parent.parent.parent / "build"


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"fork_{name}", BUILD / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def budget():
    return load("check_fork_budget")


@pytest.fixture(scope="module")
def config(budget):
    return budget.load_config()


def test_the_base_is_pinned_as_a_full_sha(config):
    assert config["base"] == "760bb7c21337abb2a2aec21434e1d208e01e6cc0"


def test_fork_code_is_recognised_by_its_paths(budget, config):
    assert budget.classify("src/RevitModelMcp.Addin/Fork/ForkLevels.cs", config) == "fork"
    assert budget.classify("src/RevitModelMcp.Core/Fork/ForkInputs.cs", config) == "fork"
    assert budget.classify("server/revit_model_mcp/fork_actions.py", config) == "fork"


def test_a_hook_is_recognised_and_an_unlisted_upstream_file_is_not(budget, config):
    assert budget.classify("src/RevitModelMcp.Addin/Application.cs", config) == "hook"
    assert (
        budget.classify("src/RevitModelMcp.Addin/Control/ActionMutations.cs", config) == "unowned"
    )


def test_the_hook_budget_counts_both_sides_of_a_change(budget, config):
    numstat = "\n".join(
        [
            "3\t1\tsrc/RevitModelMcp.Addin/Application.cs",
            "10\t0\tdocs/tools.md",
            "2\t0\tsrc/RevitModelMcp.Addin/Control/ActionMutations.cs",
        ]
    )
    hooks, other, unowned, _ = budget.changed_lines(numstat, config)
    assert hooks == {"src/RevitModelMcp.Addin/Application.cs": 4}
    assert other == {"docs/tools.md": 10}
    assert unowned == ["src/RevitModelMcp.Addin/Control/ActionMutations.cs"]


def test_a_binary_change_is_counted_by_name_not_by_lines(budget, config):
    hooks, _, _, _ = budget.changed_lines("-\t-\tsrc/RevitModelMcp.Addin/Application.cs", config)
    assert hooks == {"src/RevitModelMcp.Addin/Application.cs": 0}


def test_a_refreshed_dependency_lock_is_a_known_read_not_an_unowned_change(budget, config):
    # The dependency audit refreshes these two locks in place; the budget must
    # own that change instead of failing it as an unowned upstream file.
    assert budget.classify("server/uv.lock", config) == "read"
    assert budget.classify("server/requirements.docker.txt", config) == "read"


def test_a_removal_is_asserted_and_never_counted_as_a_read(budget, config):
    numstat = "0\t12\tserver/server.json"
    hooks, other, unowned, removed = budget.changed_lines(numstat, config)
    assert removed == ["server/server.json"]
    assert other == {}
    assert hooks == {}
    assert unowned == []


def test_every_removed_entry_states_its_reason_and_is_really_gone(config):
    repository_root = BUILD.parent
    for path, reason in config["removed"].items():
        assert reason and reason != "", path
        assert not (repository_root / path).exists(), path


def test_every_read_entry_states_its_reason(config):
    for path, reason in config["reads"].items():
        assert reason and reason != "", path


def test_the_layer_fits_its_budget_right_now(budget, config, monkeypatch):
    hooks, _, unowned, _ = budget.changed_lines(budget.numstat(config["base"]), config)
    assert sum(hooks.values()) <= config["hookBudgetLines"]
    assert unowned == []


def test_the_report_names_the_base_and_the_gap(config):
    upstream_report = load("upstream_report")
    # Compare against a ref that exists in every clone, so the test never
    # needs the upstream remote that the operational script expects.
    body = upstream_report.report(config, branch="HEAD")
    assert config["base"] in body
    assert "not in the base:" in body


def test_the_report_says_how_to_fetch_upstream_without_the_remote(config, tmp_path):
    upstream_report = load("upstream_report")
    with pytest.raises(SystemExit) as error:
        upstream_report.upstream_branch(tmp_path)
    assert "git fetch upstream" in str(error.value)
