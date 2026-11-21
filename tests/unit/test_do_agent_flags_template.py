"""Render the do-agent ExecStart drop-in and pin how settings map to flags.

Rendered directly through Jinja2, so no Ansible controller or host is needed.
"""

from pathlib import Path

from ansible.module_utils.parsing.convert_bool import boolean
from jinja2 import Environment, FileSystemLoader, StrictUndefined

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "roles" / "do" / "templates"
TEMPLATE_NAME = "etc/systemd/system/do-agent.service.d/ansible.conf.j2"
BASE = "ExecStart=/opt/digitalocean/bin/do-agent --syslog"

DEFAULTS = {
    "do_prometheus_enabled": False,
    "do_listen_address": "0.0.0.0",
    "do_prometheus_port": 9091,
    "do_log_level": "info",
    "do_labels": {},
    "do_extra_flags": [],
}


def exec_start(**overrides):
    """Return the second (effective) ExecStart line of the rendered drop-in."""
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    # Ansible's `bool` filter, which plain Jinja2 lacks.
    env.filters["bool"] = lambda value: boolean(value, strict=False)
    output = env.get_template(TEMPLATE_NAME).render(**{**DEFAULTS, **overrides})
    lines = [line for line in output.splitlines() if line.startswith("ExecStart=")]
    assert lines[0] == "ExecStart=", "the inherited ExecStart must be reset first"
    assert len(lines) == 2
    return lines[1]


def test_defaults_render_the_packaged_command():
    assert exec_start() == BASE


def test_prometheus_endpoint_maps_to_web_flags():
    assert exec_start(do_prometheus_enabled=True, do_listen_address="127.0.0.1") == (
        BASE + ' "--web.listen" "--web.listen-address=127.0.0.1:9091"'
    )


def test_string_false_does_not_open_the_metrics_endpoint():
    """A "false" string from --extra-vars must not enable --web.listen."""
    assert exec_start(do_prometheus_enabled="false") == BASE


def test_debug_log_level_maps_to_debug_flag():
    assert exec_start(do_log_level="debug") == BASE + ' "--debug"'
    assert exec_start(do_log_level="warn") == BASE


def test_labels_are_sorted_additional_labels():
    assert exec_start(do_labels={"team": "ops", "env": "prod"}) == (
        BASE + ' "--additional-label=env:prod" "--additional-label=team:ops"'
    )


def test_systemd_special_characters_are_escaped():
    line = exec_start(do_labels={"note": 'a "b" 50% $HOME \\x'})

    assert line == BASE + ' "--additional-label=note:a \\"b\\" 50%% $$HOME \\\\x"'


def test_extra_flags_are_appended_last():
    assert exec_start(do_log_level="debug", do_extra_flags=["--process-topk=50"]) == (
        BASE + ' "--debug" "--process-topk=50"'
    )
