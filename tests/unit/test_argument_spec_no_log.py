"""Pin the ``no_log`` contract for secret-bearing role options.

The argument specs are read as plain YAML, so these tests need neither an
Ansible controller nor a target host.

Scope note: ``no_log: true`` here marks an option as sensitive for task output
and ``--diff``. It does *not* censor the value in the failure output of
``validate_argument_spec`` — that action plugin writes
``validation_result.error_messages`` into ``msg`` and ``argument_errors``
without calling ``sanitize_keys``, so a value rejected by type validation is
echoed verbatim regardless. That gap is upstream in ansible-core; these tests
guard the part this collection controls.
"""

from pathlib import Path

import pytest
import yaml

ROLES_DIR = Path(__file__).resolve().parents[2] / "roles"

# Option names that carry a secret value. ``*_file`` and ``*_url`` siblings
# point at a secret rather than holding one, so they stay out.
SECRET_OPTION_NAMES = frozenset(
    {
        "password",
        "client_secret",
        "credentials",
        "bearer_token",
        "key_pem",
        "do_api_token",
        "tailscale_auth_key",
        "alloy_grafana_cloud_prometheus_token",
        "alloy_grafana_cloud_loki_token",
        "alloy_grafana_cloud_fleet_token",
    }
)


def spec_files():
    """Every role argument spec in the collection."""
    return sorted(ROLES_DIR.glob("*/meta/argument_specs.yml"))


def walk_options(options, path):
    """Yield ``(dotted_path, name, definition)`` for every nested option."""
    if not isinstance(options, dict):
        return
    for name, definition in options.items():
        if not isinstance(definition, dict):
            continue
        yield ".".join([*path, name]), name, definition
        yield from walk_options(definition.get("options"), [*path, name])


def all_options():
    """Flatten every entry point of every role spec into option records."""
    for spec_file in spec_files():
        spec = yaml.safe_load(spec_file.read_text(encoding="utf-8"))
        entry_points = (spec or {}).get("argument_specs") or {}
        for entry_point, body in entry_points.items():
            prefix = [spec_file.parts[-3], entry_point]
            yield from (
                (spec_file, *record)
                for record in walk_options((body or {}).get("options"), prefix)
            )


@pytest.mark.parametrize("spec_file", spec_files(), ids=lambda p: p.parts[-3])
def test_spec_parses(spec_file):
    """Each argument spec is valid YAML with an argument_specs mapping."""
    spec = yaml.safe_load(spec_file.read_text(encoding="utf-8"))

    assert isinstance(spec.get("argument_specs"), dict)


def test_every_secret_option_sets_no_log():
    """No secret-bearing option is declared without ``no_log: true``."""
    unmasked = [
        f"{spec_file.parts[-3]}: {dotted}"
        for spec_file, dotted, name, definition in all_options()
        if name in SECRET_OPTION_NAMES and definition.get("no_log") is not True
    ]

    assert not unmasked, "secret options without no_log: true: " + ", ".join(unmasked)


def test_file_and_url_siblings_stay_unmasked():
    """``*_file``/``*_url`` options point at secrets and must stay readable.

    Masking these would censor a path or endpoint that is useful in output and
    is not itself sensitive.
    """
    wrongly_masked = [
        f"{spec_file.parts[-3]}: {dotted}"
        for spec_file, dotted, name, definition in all_options()
        if name.endswith(("_file", "_url")) and definition.get("no_log") is True
    ]

    assert not wrongly_masked, "no_log on a non-secret pointer option: " + ", ".join(
        wrongly_masked
    )


def test_secret_options_are_actually_present():
    """Guard against the sweep silently matching nothing."""
    found = {
        record[2] for record in all_options() if record[2] in SECRET_OPTION_NAMES
    }

    assert {"password", "bearer_token", "client_secret"} <= found


@pytest.mark.parametrize(
    ("role", "toggle", "task_file"),
    [
        ("alloy", "alloy_no_log_config", "configure.yml"),
        ("alloy", "alloy_no_log_env_file", "configure.yml"),
        ("do", "do_no_log_api_token", "configure.yml"),
        ("tailscale", "tailscale_no_log_auth_key", "configure.yml"),
    ],
)
def test_no_log_toggle_is_declared_and_used(role, toggle, task_file):
    """Each debugging toggle has a default and gates at least one task."""
    defaults = yaml.safe_load(
        (ROLES_DIR / role / "defaults" / "main.yml").read_text(encoding="utf-8")
    )
    tasks = (ROLES_DIR / role / "tasks" / task_file).read_text(encoding="utf-8")

    assert defaults.get(toggle) is True, f"{toggle} must default to true"
    assert toggle in tasks, f"{toggle} gates no task in {role}/{task_file}"
