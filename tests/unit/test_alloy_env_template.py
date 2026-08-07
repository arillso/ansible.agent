"""Render the alloy environment-file template and pin the variable naming contract.

The template is rendered directly through Jinja2, so these tests need neither an
Ansible controller nor a target host.
"""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, StrictUndefined

TEMPLATE_DIR = (
    Path(__file__).resolve().parents[2] / "roles" / "alloy" / "templates"
)
TEMPLATE_NAME = "etc/default/alloy.j2"

# Values the template must render regardless of the credential variables.
BASE_VARS = {
    "alloy_log_level": "info",
    "alloy_log_format": "logfmt",
    "alloy_server_http_listen_address": "127.0.0.1",
    "alloy_port": 12345,
    "alloy_server_grpc_listen_address": "127.0.0.1",
    "alloy_grpc_port": 12346,
    "alloy_storage_path": "/var/lib/alloy",
    "alloy_clustering_enabled": False,
}

# Rendered-value markers. Deliberately not credential-shaped: secret scanners
# flag short "<word>-token" literals as candidate API keys.
CREDENTIAL_VARS = {
    "alloy_grafana_cloud_prometheus_user": "rendered-prometheus-username",
    "alloy_grafana_cloud_prometheus_token": "rendered-prometheus-credential",
    "alloy_grafana_cloud_loki_user": "rendered-loki-username",
    "alloy_grafana_cloud_loki_token": "rendered-loki-credential",
    "alloy_grafana_cloud_fleet_user": "rendered-fleet-username",
    "alloy_grafana_cloud_fleet_token": "rendered-fleet-credential",
}

# The pre-migration names, which the template must no longer read.
LEGACY_NAMES = [name.removeprefix("alloy_") for name in CREDENTIAL_VARS]


def render(**overrides):
    """Render the template with StrictUndefined so unset reads raise."""
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    context = {**BASE_VARS, **overrides}
    return env.get_template(TEMPLATE_NAME).render(**context)


def test_prefixed_credentials_render():
    """The prefixed variables reach the rendered environment file."""
    output = render(**CREDENTIAL_VARS, alloy_remotecfg_enabled=True)

    assert "GRAFANA_CLOUD_PROMETHEUS_TOKEN=rendered-prometheus-credential" in output
    assert "GRAFANA_CLOUD_PROMETHEUS_USER=rendered-prometheus-username" in output
    assert "GRAFANA_CLOUD_LOKI_TOKEN=rendered-loki-credential" in output
    assert "GRAFANA_CLOUD_LOKI_USER=rendered-loki-username" in output


def test_template_reads_no_unprefixed_names():
    """No unprefixed grafana_cloud_* name is left in the template source."""
    source = (TEMPLATE_DIR / TEMPLATE_NAME).read_text(encoding="utf-8")

    for legacy in LEGACY_NAMES:
        assert f"{{{{ {legacy}" not in source, f"template still reads {legacy}"
        assert f"if {legacy}" not in source, f"template still guards on {legacy}"


def test_legacy_names_are_ignored():
    """Values supplied under the old names do not reach the output."""
    legacy_values = {name: f"legacy-{name}" for name in LEGACY_NAMES}
    output = render(**legacy_values, alloy_remotecfg_enabled=True)

    assert "legacy-" not in output


def test_credentials_omitted_when_unset():
    """Without credentials the token keys are absent, not rendered empty."""
    output = render(alloy_remotecfg_enabled=True)

    assert "GRAFANA_CLOUD_PROMETHEUS_TOKEN" not in output
    assert "GRAFANA_CLOUD_LOKI_TOKEN" not in output
    assert "GRAFANA_CLOUD_FLEET_TOKEN" not in output


@pytest.mark.parametrize(
    ("variable", "placeholder", "key"),
    [
        (
            "alloy_grafana_cloud_prometheus_token",
            "your-grafana-cloud-prometheus-token",
            "GRAFANA_CLOUD_PROMETHEUS_TOKEN",
        ),
        (
            "alloy_grafana_cloud_loki_token",
            "your-grafana-cloud-loki-token",
            "GRAFANA_CLOUD_LOKI_TOKEN",
        ),
        (
            "alloy_grafana_cloud_fleet_token",
            "your-grafana-cloud-fleet-token",
            "GRAFANA_CLOUD_FLEET_TOKEN",
        ),
    ],
)
def test_placeholder_values_are_suppressed(variable, placeholder, key):
    """The shipped placeholder values never reach the environment file."""
    output = render(**{variable: placeholder}, alloy_remotecfg_enabled=True)

    assert key not in output


def test_fleet_credentials_require_remotecfg():
    """Fleet credentials render only when remotecfg is enabled."""
    disabled = render(**CREDENTIAL_VARS, alloy_remotecfg_enabled=False)
    enabled = render(**CREDENTIAL_VARS, alloy_remotecfg_enabled=True)

    assert "GRAFANA_CLOUD_FLEET_TOKEN" not in disabled
    assert "GRAFANA_CLOUD_FLEET_TOKEN=rendered-fleet-credential" in enabled
    assert "GRAFANA_CLOUD_FLEET_USER=rendered-fleet-username" in enabled


def test_base_settings_render_without_credentials():
    """The non-credential part of the file is independent of the migration."""
    output = render(alloy_remotecfg_enabled=False)

    assert "ALLOY_LOG_LEVEL=info" in output
    assert "ALLOY_SERVER_HTTP_LISTEN_ADDRESS=127.0.0.1:12345" in output
    assert "ALLOY_STORAGE_PATH=/var/lib/alloy" in output
