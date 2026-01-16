# Changelog

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
and [human-readable changelog](https://keepachangelog.com/en/1.0.0/).

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

#### Documentation & Development Workflow

- **EditorConfig** - Consistent code formatting across editors (.editorconfig)
- **GitHub Templates** - Issue templates for bug reports, documentation, and feature requests
- **Pull Request Template** - Standardized PR description format (.github/pull_request_template.md)
- **CODEOWNERS** - Automated review assignments (.github/CODEOWNERS)
- **Contributing Guidelines** - Comprehensive development guidelines (CONTRIBUTING.md)
- **Project Instructions** - AI-assisted development documentation (AGENTS.md, CLAUDE.md)
- **Test Configuration** - pytest configuration for unit tests (pytest.ini)
- **Python Requirements** - Development dependencies (requirements.txt)
- **yamllint Configuration** - YAML linting rules (.yamllint)

#### CI/CD Improvements

- **Unified CI Workflow** - All-in-one workflow for linting, tests, and build (.github/workflows/ci.yml)
- **Renovate** - Automated dependency updates (.github/renovate.json)
- **Enhanced Publish Workflow** - Improved Galaxy publishing with changelog integration

#### Molecule Tests

- **Alloy Role** - Complete molecule test suite with Docker driver
- **DO Role** - Complete molecule test suite with Docker driver
- **Tailscale Role** - Complete molecule test suite with Docker driver

### Changed

#### Documentation

- **README.md** - Updated with all three roles and improved examples
- **LICENSE** - Updated copyright year to 2022-2026
- **galaxy.yml** - Updated metadata, dependencies, and tags
- **meta/runtime.yml** - Updated to require Ansible 2.15+

#### CI/CD

- **.gitignore** - Streamlined and reorganized
- **publish.yml** - Enhanced with better error handling and changelog integration

### Removed

#### Development Configuration

- **.pre-commit-config.yaml** - Removed pre-commit hooks in favor of CI-based linting
- **dependabot.yml** - Replaced by Renovate
- **renovate.json** (root) - Moved to .github/renovate.json
- **linter.yml** - Consolidated into ci.yml workflow

## [1.0.0] - 2025-11-20

### Added

#### Alloy Role (New)

- **Grafana Alloy role** - Complete observability agent replacing Grafana Agent
    - Prometheus metrics collection with advanced relabeling support
    - Integrated Node Exporter with 50+ configurable collectors
    - Loki log collection from files and systemd journal
    - OpenTelemetry (OTLP) receiver and exporters for traces
    - Custom exporters support including Tailscale metrics integration
    - Grafana Cloud Fleet integration for remote configuration management
    - Frontend Observability (Faro) for Real User Monitoring (RUM)
    - Clustering support for high availability deployments
    - Environment variable-based credential management for improved security
    - Security-hardened systemd service configuration
    - Modular configuration architecture with reusable components
    - Health check validation with automatic retry logic
    - Comprehensive argument specifications (1128 lines)
    - Support for Ubuntu 20.04+, Debian 11+, RHEL/CentOS 8+

#### Tailscale Role (New)

- **Tailscale VPN role** - Mesh networking and secure connectivity
    - WireGuard-based VPN with automatic mesh network topology
    - Exit node support for routing internet traffic
    - Subnet routing for accessing private networks
    - SSH over Tailscale for secure remote access
    - Web UI and metrics endpoint (port 5252)
    - App connector functionality for application-level access
    - Stateful packet filtering support
    - Local facts for status monitoring and automation
    - Connectivity verification tasks
    - Service overrides for systemd customization
    - Multiple entry points (install, configure, service, verify, facts)
    - Comprehensive argument specifications (432 lines)
    - Support for Ubuntu 18.04+, Debian 10+, RHEL family, Alpine, Arch Linux

#### Collection Enhancements

- Production-ready collection metadata with version 1.0.0
- Comprehensive README with installation instructions and examples
- Example playbooks for all roles (individual and combined usage)
- Dependency on `arillso.system` collection for package management
- Updated tags for better discoverability (alloy, tailscale, digitalocean, monitoring, observability, vpn)

### Changed

#### DO Role (Restructured)

- **Complete restructuring** of DigitalOcean Agent role with improved architecture
    - Modular task organization (install.yml, configure.yml, service.yml)
    - OS-specific variables (Debian.yml, RedHat.yml) for better maintainability
    - Enhanced handlers for service management
    - Security-hardened systemd service configuration
    - Health check validation after installation
    - Improved documentation with zero-configuration emphasis
    - Support for optional advanced configuration
    - Updated to Ansible 2.15+ requirements

#### Collection Metadata

- Collection name corrected from `arillso.agents` to `arillso.agent`
- Description updated to mention all three agents specifically
- Dependencies updated: removed Windows-specific collections (chocolatey, ansible.windows)
- Dependencies updated: added `arillso.system` collection (required for Alloy role)
- Author information maintained and verified
- Repository URLs and documentation links updated

### Deprecated

- **Grafana Agent role** - Replaced by Grafana Alloy role (see Migration Guide below)

### Removed

- **Grafana Agent role** - Completely removed in favor of Grafana Alloy
    - All Grafana Agent task files (Debian, RedHat, Windows variants)
    - All Grafana Agent templates (Linux and Windows configurations)
    - All Grafana Agent metadata and documentation
    - All Grafana Agent handlers

- **Old DO role structure** - Replaced with modular architecture
    - `tasks/install_do_debian.yml` - replaced by `tasks/install.yml` with OS-specific vars
    - `tasks/install_do_redhat.yml` - replaced by `tasks/install.yml` with OS-specific vars

- **Repository configuration files**
    - `.gitignore` - Removed (needs recreation)
    - `.pre-commit-config.yaml` - Removed (optional, can be recreated)

### Migration Guide

#### Migrating from Grafana Agent to Grafana Alloy

Grafana Alloy is the successor to Grafana Agent and provides enhanced features and better performance. To migrate:

**1. Update your playbook:**

```yaml
# Old (Grafana Agent)
- role: arillso.agent.grafana
  vars:
      grafana_agent_prometheus_url: "https://prometheus.example.com"

# New (Grafana Alloy)
- role: arillso.agent.alloy
  vars:
      alloy_prometheus_enabled: true
      alloy_prometheus_remote_write_url: "https://prometheus.example.com/api/v1/write"
```

**2. Key variable name changes:**

| Grafana Agent                  | Grafana Alloy                                     | Notes                                     |
| ------------------------------ | ------------------------------------------------- | ----------------------------------------- |
| `grafana_agent_prometheus_url` | `alloy_prometheus_remote_write_url`               | Must include `/api/v1/write` endpoint     |
| `grafana_agent_loki_url`       | `alloy_loki_url`                                  | Must include `/loki/api/v1/push` endpoint |
| `grafana_agent_enabled`        | `alloy_prometheus_enabled` / `alloy_loki_enabled` | Separate flags for each component         |
| `grafana_agent_config`         | `alloy_config_*` variables                        | More granular configuration options       |

**3. Configuration improvements in Alloy:**

- **Environment variables**: API keys and credentials are now stored in `/etc/default/alloy` instead of inline in config
- **Modular configuration**: Configuration is split into modules (prometheus, loki, otel, etc.)
- **Advanced relabeling**: Dedicated `prometheus.relabel` components for better metric processing
- **Health checks**: Automatic validation after installation with retry logic

**4. New features available:**

- OpenTelemetry support (traces)
- Grafana Cloud Fleet integration
- Clustering for high availability
- Frontend Observability (Faro)
- Tailscale metrics integration
- Enhanced Node Exporter with 50+ collectors

**5. Service changes:**

```bash
# Old service name
systemctl status grafana-agent

# New service name
systemctl status alloy
```

**6. Configuration file locations:**

- Old: `/etc/grafana-agent.yaml`
- New: `/etc/alloy/config.alloy` (Alloy River format)

**7. Testing your migration:**

```yaml
# Test playbook for migration
- name: Migrate from Grafana Agent to Alloy
  hosts: monitoring
  become: true

  tasks:
      # Optional: Stop and disable old Grafana Agent
      - name: Stop Grafana Agent
        systemd:
            name: grafana-agent
            state: stopped
            enabled: false
        ignore_errors: true

      # Install Alloy
      - include_role:
            name: arillso.agent.alloy
        vars:
            alloy_prometheus_enabled: true
            alloy_prometheus_remote_write_url: "{{ old_prometheus_url }}/api/v1/write"
            alloy_loki_enabled: true
            alloy_loki_url: "{{ old_loki_url }}/loki/api/v1/push"
```

For detailed configuration examples, see the [Alloy role README](roles/alloy/README.md).

### Security

- **Environment variable integration**: Credentials are now loaded from environment files (`/etc/default/alloy`) instead of being embedded in configuration files
- **Security-hardened systemd services**: All roles now use systemd service hardening features
- **Improved credential rotation**: Simplified process for updating API keys and tokens

### Platform Support

#### Supported Operating Systems

**Alloy Role:**

- Ubuntu 20.04, 22.04, 24.04
- Debian 11, 12
- RHEL/CentOS 8, 9

**DigitalOcean Agent Role:**

- Ubuntu 20.04, 22.04, 24.04
- Debian 11, 12
- RHEL/CentOS 8, 9

**Tailscale Role:**

- Ubuntu 18.04, 20.04, 22.04, 24.04
- Debian 10, 11, 12
- RedHat, CentOS, Rocky, AlmaLinux, Fedora
- Alpine Linux (package-only mode)
- Arch Linux (package-only mode)

### Contributors

- Simon Baerlocher (@sbaerlocher) - Initial release and all role development

---

## [0.x.x] - Previous Versions

See: <https://github.com/arillso/ansible.agent/releases>

[Unreleased]: https://github.com/arillso/ansible.agent/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/arillso/ansible.agent/releases/tag/v1.0.0
