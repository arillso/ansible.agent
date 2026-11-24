"""Keep ``argument_specs.yml`` defaults in step with ``defaults/main.yml``.

guide.arillso.io renders the role pages from the argument specs, so a
``default:`` missing there hides the real value from the docs. The specs are
documentation only: ``validate_argument_spec`` does not set variables, the
values come from ``defaults/main.yml``. These tests read both files as plain
YAML and need neither an Ansible controller nor a target host.
"""

from pathlib import Path

import pytest
import yaml

ROLES_DIR = Path(__file__).resolve().parents[2] / "roles"
ROLES = ("alloy", "do", "tailscale")


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_spec(role):
    return load_yaml(ROLES_DIR / role / "meta" / "argument_specs.yml")[
        "argument_specs"
    ]


def is_static(value):
    """True unless a Jinja expression anywhere in the value resolves at runtime."""
    if isinstance(value, str):
        return "{{" not in value and "{%" not in value
    if isinstance(value, dict):
        return all(is_static(v) for v in value.values())
    if isinstance(value, list):
        return all(is_static(v) for v in value)
    return True


def missing_defaults(options, values, path):
    """Yield a message per option whose spec default differs from its value.

    Recurses into dict sub-options so nested defaults are covered too. List
    elements are user input, not defaults, so lists are compared as a whole.
    """
    for name, value in values.items():
        definition = options.get(name)
        if not isinstance(definition, dict) or definition.get("required"):
            continue
        dotted = f"{path}.{name}"
        if is_static(value):
            if "default" not in definition:
                yield f"{dotted}: no default (expected {value!r})"
            elif definition["default"] != value:
                yield f"{dotted}: default {definition['default']!r} != {value!r}"
        if isinstance(value, dict) and isinstance(definition.get("options"), dict):
            yield from missing_defaults(definition["options"], value, dotted)


def walk_options(options, path):
    for name, definition in (options or {}).items():
        if isinstance(definition, dict):
            yield f"{path}.{name}", definition
            yield from walk_options(definition.get("options"), f"{path}.{name}")


@pytest.mark.parametrize("role", ROLES)
def test_static_defaults_are_documented(role):
    """Every static value in defaults/main.yml appears as the spec default."""
    values = load_yaml(ROLES_DIR / role / "defaults" / "main.yml")
    drift = [
        message
        for entry_point, body in load_spec(role).items()
        for message in missing_defaults(
            (body or {}).get("options") or {}, values, f"{role}.{entry_point}"
        )
    ]

    assert not drift, "spec defaults out of step:\n" + "\n".join(drift)


@pytest.mark.parametrize("role", ROLES)
def test_required_options_have_no_default(role):
    """``required`` and ``default`` together make ansible-core raise."""
    both = [
        dotted
        for entry_point, body in load_spec(role).items()
        for dotted, definition in walk_options(
            (body or {}).get("options"), f"{role}.{entry_point}"
        )
        if definition.get("required") and "default" in definition
    ]

    assert not both, "required options with a default: " + ", ".join(both)

