"""Render the alloy systemd drop-in and pin the resource-limit and log-file lines."""

import os.path
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

TEMPLATE_DIR = (
    Path(__file__).resolve().parents[2] / "roles" / "alloy" / "templates"
)
TEMPLATE_NAME = "etc/systemd/system/alloy.service.d/override.conf.j2"

BASE_VARS = {
    "alloy_user": "alloy",
    "alloy_group": "alloy",
    "alloy_config_file": "/etc/alloy/config.alloy",
    "alloy_storage_path": "/var/lib/alloy",
    "alloy_web_server_enabled": True,
    "alloy_server_http_listen_address": "0.0.0.0",
    "alloy_port": 12345,
    "alloy_grpc_server_enabled": False,
    "alloy_env_file": "/etc/default/alloy",
    "alloy_log_file": "",
    "alloy_max_memory": "",
    "alloy_max_cpu": "",
}


def render(**overrides):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), undefined=StrictUndefined)
    env.filters["dirname"] = os.path.dirname  # Ansible filter, not core Jinja
    return env.get_template(TEMPLATE_NAME).render(**{**BASE_VARS, **overrides})


def test_defaults_render_no_empty_limits():
    output = render()

    assert "MemoryMax" not in output
    assert "MemoryLimit" not in output
    assert "CPUQuota" not in output
    assert "StandardError" not in output


def test_limits_use_memory_max():
    output = render(alloy_max_memory="256M", alloy_max_cpu="50%")

    assert "MemoryMax=256M" in output
    assert "CPUQuota=50%" in output
    assert "MemoryLimit" not in output


def test_log_file_redirects_output():
    output = render(alloy_log_file="/var/log/alloy/alloy.log")

    assert "ReadWritePaths=/var/log/alloy" in output
    assert "StandardOutput=append:/var/log/alloy/alloy.log" in output
    assert "StandardError=append:/var/log/alloy/alloy.log" in output


def test_ipv6_listen_address_is_bracketed():
    output = render(alloy_server_http_listen_address="::")

    assert "--server.http.listen-addr=[::]:12345" in output


def test_bracketed_listen_address_is_kept():
    output = render(alloy_server_http_listen_address="[::1]")

    assert "--server.http.listen-addr=[::1]:12345" in output
