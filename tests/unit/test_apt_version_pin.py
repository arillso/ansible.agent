"""Unit tests for the apt_version_pin filter.

The fixtures mirror the version strings the upstream apt repositories publish:
Grafana appends a Debian revision (1.21.3-1), Tailscale and DigitalOcean do not.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "plugins" / "filter"))

from apt_filters import apt_version_pin  # noqa: E402

ALLOY = [
    " alloy | 1.21.30-1 | https://apt.grafana.com stable/main amd64 Packages",
    " alloy | 1.21.3-1 | https://apt.grafana.com stable/main amd64 Packages",
    " alloy | 1.21.2-1 | https://apt.grafana.com stable/main amd64 Packages",
]

TAILSCALE = [
    " tailscale | 1.104.5 | https://pkgs.tailscale.com/stable/debian bookworm/main amd64 Packages",
    " tailscale | 1.104.4 | https://pkgs.tailscale.com/stable/debian bookworm/main amd64 Packages",
]

EPOCH = [" pkg | 2:3.18.16~bpo12+1 | https://example.invalid main amd64 Packages"]


def test_revision_suffix():
    assert apt_version_pin(ALLOY, "1.21.3") == "1.21.3-1"


def test_bare_version():
    assert apt_version_pin(TAILSCALE, "1.104.4") == "1.104.4"


def test_epoch_and_tilde():
    assert apt_version_pin(EPOCH, "3.18.16") == "2:3.18.16~bpo12+1"


def test_no_prefix_match():
    assert apt_version_pin(ALLOY, "1.21") is None
    assert apt_version_pin(TAILSCALE, "1.104") is None


def test_dots_are_literal():
    assert apt_version_pin(TAILSCALE, "1X104X4") is None


def test_missing_version_and_empty_input():
    assert apt_version_pin(ALLOY, "9.9.9") is None
    assert apt_version_pin([], "1.21.3") is None
    assert apt_version_pin(ALLOY, "") is None
