# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **CI**: the `arillso/.github` reusable workflows are pinned to `2026-08-17`
  and every `python_version` input is raised from `3.13` to `3.14`. The new
  `ci-ansible-collection` derives the controller interpreter from the ansible
  branch (`stable-2.20` and `devel` on 3.14, older branches on 3.13) and
  ignores the input for known branches, so sanity now covers 3.14 while the
  input only drives the lint and molecule jobs. The supported ansible range in
  `meta/runtime.yml` is unchanged.

## [2.0.0] - 2026-08-17

### Added

- **Master switches (all roles)**: `alloy_enabled`, `do_enabled`, and
  `tailscale_enabled` (all `bool`, default `true`) gate every dispatcher
  include in the respective `tasks/main.yml`. Setting one to `false` skips
  the whole role instead of requiring per-task `when` conditions.
- **Alloy**: `alloy_remotecfg` now declares the `authorization` and `oauth2`
  blocks in `meta/argument_specs.yml`. Both were rendered by
  `templates/etc/alloy/modules/remotecfg.j2` but undocumented, so their
  secrets passed through validation undeclared and unmasked. The top-level
  `tls_config` gains the `ca_pem`, `cert_file`, `cert_pem`, `key_file`,
  `key_pem`, `server_name`, and `min_version` options the template already
  renders.
- `.python-version`, consumed by the release workflow, which reads this file
  when no `python_version` input is passed — `tag.yml` passes none. It now
  holds `3.14`, matching `arillso/ansible.system` and `arillso/ansible.container`,
  which both pin `3.14.7`. Note that CI does not read this file: the `ci` and
  molecule jobs in `pull-request.yml` and `merge.yml` pass a `python_version` of
  `3.13` explicitly, so the release artifact is built on a newer interpreter
  than the one CI exercises. Raising the CI jobs to `3.14` is tracked separately
  — `ansible-test` in ansible-core 2.18 lists `3.11`–`3.13` as controller
  versions, so that bump needs verifying against the reusable workflow first.
- **CI — nightly security scanning**: `nightly-security.yml` runs daily at
  02:00 UTC and now carries three jobs instead of one. `security-config` adds a
  Trivy `scan-type: config` pass for IaC misconfigurations, complementing the
  `scan-type: fs` dependency scan in `ci-ansible-collection`; `security-sbom`
  generates a filesystem SBOM as an inventory artifact. Each job declares its
  own permissions — a called workflow can only narrow the caller's scopes, never
  widen them, so the elevated `security-events: write` and `contents: write`
  stay on the jobs that need them instead of applying workflow-wide.
- **CI — unit tests**: the `ci` job passes `enable_unit_tests: true` in both
  `pull-request.yml` and `merge.yml`, so `tests/unit/` runs on pull requests and
  on pushes to `main`.
- **CI — combined molecule scenario**: `molecule-multi-role` runs the
  `extensions/molecule/multi-role` scenario, which deploys `alloy`, `do` and
  `tailscale` together on one host.
- **Makefile**: the `test` target is split into `test-unit` and `test-molecule`,
  so unit tests can run without spinning up molecule scenarios.

### Removed

- **Developer Tooling**: the seven scanner configs `.checkov.yml`, `.grype.yaml`,
  `.jscpd.json`, `.kics.json`, `.markdown-link-check.json`, `.secretlintrc.json`
  and `.trivy.yaml` are gone. None of the tools they configure runs in the
  reusable CI: checkov, grype, jscpd, kics, markdown-link-check and secretlint
  appear in no workflow of `arillso/.github`, and `security-secrets.yml` runs
  Gitleaks, TruffleHog and pattern detection only. Trivy does run, but reads its
  config through the `trivy_config` input, which defaults to an empty string and
  is passed by no workflow here — and it auto-discovers `trivy.yaml`, not the
  dotted `.trivy.yaml`. `.gitleaks.toml` stays, because Gitleaks auto-loads it.
- **DO**: the three feature flags `do_metrics_enabled`, `do_logs_enabled` and
  `do_insights_enabled` are gone from `defaults/main.yml` and
  `meta/argument_specs.yml`. They were declared and documented but read by no
  task and no template, so setting one to `false` changed nothing and raised no
  error. `do-agent` has no upstream switch for metrics, logs or insights as a
  whole — only per-collector flags such as `no-collector.processes` — so there
  is nothing to wire them to. Removing them has no effect on behaviour. The
  master switch `do_enabled` is unaffected and still gates the whole role.
- **Alloy (breaking)**: the six unprefixed Grafana Cloud variables the role read
  are replaced by role-prefixed names. They were never declared in
  `defaults/main.yml` or `meta/argument_specs.yml` and worked only through
  `| default('')` guards in the template, so no documented interface changes.
  Rename them in your inventory:

  | Old                              | New                                    |
  | -------------------------------- | -------------------------------------- |
  | `grafana_cloud_prometheus_user`  | `alloy_grafana_cloud_prometheus_user`  |
  | `grafana_cloud_prometheus_token` | `alloy_grafana_cloud_prometheus_token` |
  | `grafana_cloud_loki_user`        | `alloy_grafana_cloud_loki_user`        |
  | `grafana_cloud_loki_token`       | `alloy_grafana_cloud_loki_token`       |
  | `grafana_cloud_fleet_user`       | `alloy_grafana_cloud_fleet_user`       |
  | `grafana_cloud_fleet_token`      | `alloy_grafana_cloud_fleet_token`      |

  The `GRAFANA_CLOUD_*` keys inside the environment file are unchanged — Alloy
  itself reads those. All seven variables are now declared in
  `defaults/main.yml` and `meta/argument_specs.yml`, the three tokens with
  `no_log: true`.

### Fixed

- **Alloy**: add `no_log` to the `Create environment file` task, which renders
  the Grafana Cloud tokens. Without it the credentials appeared in the Ansible
  output at raised verbosity. The new `alloy_no_log_env_file` toggle (default
  `true`) allows disabling it for a single debugging run, mirroring
  `tailscale_no_log_auth_key`.
- **Alloy remotecfg secret exposure**: the main config task renders the
  `alloy_remotecfg` secrets (`basic_auth.password`,
  `authorization.credentials`, `bearer_token`, `oauth2.client_secret`) into
  `config.alloy` and set no `no_log`, so the values appeared in the Ansible
  output at raised verbosity. The task now honours the new
  `alloy_no_log_config` toggle (default `true`), mirroring
  `alloy_no_log_env_file`. The same options additionally carry `no_log: true`
  in the argument spec, which marks them as sensitive for task output and
  `--diff`. Note that this does **not** censor them in the failure output of
  `validate_argument_spec`: that action plugin writes
  `validation_result.error_messages` straight into `msg` and
  `argument_errors` without calling `sanitize_keys`, so a value rejected by
  type validation is echoed verbatim regardless of `no_log` (verified against
  ansible-core 2.21.1). Closing that gap requires a fix upstream in
  ansible-core, not in this collection.
- **Alloy remaining secret options**: the `basic_auth.password` and
  `bearer_token` options of `alloy_prometheus_remote_write`,
  `alloy_loki_clients`, and `alloy_custom_exporters` now carry `no_log: true`
  as well. They are rendered into `config.alloy` by the same task and are
  covered by the `alloy_no_log_config` toggle above.
- **Tailscale**: `tailscale_auth_key` carries `no_log: true` in the argument
  spec. The key was declared sensitive at task level only, so the spec did
  not mark it as such for the rest of the role.
- **Alloy**: tighten `/etc/default/alloy` from mode `0640` to `0600`. The file
  holds the Grafana Cloud credentials and is read by systemd as root, so group
  read access was never needed.
- **Molecule (all roles)**: add the missing `side_effect.yml` play to the
  `alloy`, `do`, and `tailscale` default scenarios. Their `test_sequence`
  referenced a `side_effect` step with no matching file, so `molecule test`
  failed before reaching `verify`.
- **Alloy argument_specs**: align the `alloy_version` default (`1.13.2`) with
  `defaults/main.yml` (`1.17.0`) so the documented and effective defaults match.
- **DO role token exposure**: the rendered agent config carried
  `do_api_token` while being written world-readable (`0644`) and keeping
  backup copies, and neither template task set `no_log`. The config is now
  `0600`, backups are gone, both token-rendering tasks honour the new
  `do_no_log_api_token` toggle (default `true`), and `do_api_token` carries
  `no_log: true` in the argument spec again.
  This also corrects the note under 1.0.1 claiming `no_log` is not permitted
  in Ansible's `argument_specs` schema. It is: `ansible-lint` declares
  `no_log` as a boolean role-arg-spec option, argument-spec validation passes
  with it, and `ansible-galaxy collection build` succeeds.
- **DO role leftover backups**: dropping `backup: true` stopped new plaintext
  copies but left the existing ones in place, so hosts provisioned before that
  fix still carried the token in world-readable `/etc/do-agent/do-agent.yaml.*~`
  files. `configure.yml` now finds and removes them on every run, independently
  of `do_custom_config_enabled`, so the cleanup also reaches hosts where custom
  config has since been turned off. The pattern is limited to Ansible's own
  backup suffix (trailing `~`) so package-manager artifacts such as
  `.dpkg-dist` or `.rpmnew` are left untouched.

### Changed

- **BREAKING — handler topic namespacing (`alloy`, `do`, `tailscale`)**: all
  handler `listen:` topics are now prefixed with their role. The three roles
  each listened on the bare topic `reload systemd`, so loading them in one play
  made a single `notify` fire the handlers of all three. A `notify` to a topic
  with no matching handler is ignored rather than an error, so consumer plays
  notifying the old bare topics silently stop triggering and must be updated.

  | Role        | Old                       | New                                  |
  | ----------- | ------------------------- | ------------------------------------ |
  | `alloy`     | `reload systemd`          | `alloy: reload systemd`              |
  | `alloy`     | `restart alloy`           | `alloy: restart alloy`               |
  | `alloy`     | `restart grafana alloy`   | `alloy: restart grafana alloy`       |
  | `alloy`     | `update apt cache`        | `alloy: update apt cache`            |
  | `do`        | `reload systemd`          | `do: reload systemd`                 |
  | `do`        | `restart do agent`        | `do: restart do agent`               |
  | `tailscale` | `reload systemd`          | `tailscale: reload systemd`          |
  | `tailscale` | `restart tailscaled`      | `tailscale: restart tailscaled`      |
  | `tailscale` | `reload tailscale config` | `tailscale: reload tailscale config` |
  | `tailscale` | `refresh ansible facts`   | `tailscale: refresh ansible facts`   |

  Handler names stay descriptive sentences; only the `listen:` topics carry
  the prefix, matching the convention in `arillso/ansible.system`. This also
  resolves a case mismatch in the `tailscale` role, where one task notified
  the handler by name (`Refresh ansible facts`) while every other call site
  used the lowercase listen topic.

- **BREAKING — boolean variable naming (`alloy`)**: 10 boolean variables
  moved from the `*_enable_*` prefix form to the `*_enabled` suffix form. The
  old names are gone; there is no deprecation alias, so playbooks setting them
  silently lose the setting and must be updated. This also fixes the `alloy`
  README Quick Start, which already documented the `*_enabled` names — none of
  which existed, so copying it produced an Alloy with nothing enabled.

  | Role    | Old                                   | New                                    |
  | ------- | ------------------------------------- | -------------------------------------- |
  | `alloy` | `alloy_enable_web_server`             | `alloy_web_server_enabled`             |
  | `alloy` | `alloy_enable_grpc_server`            | `alloy_grpc_server_enabled`            |
  | `alloy` | `alloy_server_http_enable_pprof`      | `alloy_server_http_pprof_enabled`      |
  | `alloy` | `alloy_enable_prometheus`             | `alloy_prometheus_enabled`             |
  | `alloy` | `alloy_enable_loki`                   | `alloy_loki_enabled`                   |
  | `alloy` | `alloy_enable_otel`                   | `alloy_otel_enabled`                   |
  | `alloy` | `alloy_enable_otel_processors`        | `alloy_otel_processors_enabled`        |
  | `alloy` | `alloy_enable_advanced_node_exporter` | `alloy_advanced_node_exporter_enabled` |
  | `alloy` | `alloy_enable_journal_monitoring`     | `alloy_journal_monitoring_enabled`     |
  | `alloy` | `alloy_enable_remotecfg`              | `alloy_remotecfg_enabled`              |

  The `enable_start_time_metrics`, `enable_task_metrics` and
  `enable_restarts_metrics` keys inside `alloy_node_exporter_config.systemd`
  are upstream Alloy configuration and are unchanged. The `tailscale` role
  already used the suffix form and is untouched by this rename — see the
  separate `tailscale_daemon_enabled` entry below.

- **BREAKING — Tailscale**: the daemon config key `tailscale_enabled` is
  renamed to `tailscale_daemon_enabled`. It still sets `"enabled"` in
  `/etc/tailscale/config.json` and keeps its `str` type and empty default.
  The freed name `tailscale_enabled` is now the role master switch (`bool`,
  default `true`). Anyone who set `tailscale_enabled` to control the daemon
  config must rename it to `tailscale_daemon_enabled`; leaving it in place
  no longer writes the daemon config and instead toggles the whole role.

- **All roles**: every top-level fact reference is replaced by its
  `ansible_facts` equivalent — `ansible_os_family` becomes
  `ansible_facts['os_family']`, `ansible_hostname` becomes
  `ansible_facts['hostname']`, and the `ansible_distribution*` family becomes
  `ansible_facts['distribution*']`. `ansible-core` deprecated the
  `INJECT_FACTS_AS_VARS` default of `True` and drops the automatic top-level
  injection in version 2.24, which would leave the unprefixed names undefined
  and break the roles. Variable names only, no behaviour change.
  `ansible_local` keeps its name: it is exempt from the deprecation and stays
  at the top level even when read from `ansible_facts`.

- **Renovate**: the custom regex manager now also scans
  `roles/*/meta/argument_specs.yml`, and the `*_version` defaults in the
  `alloy`, `do`, and `tailscale` specs carry `# renovate:` comments, so future
  upstream releases bump both `defaults/main.yml` and the argument spec in one
  PR. The spec defaults had drifted because nothing tracked them — realigned
  `do_version` (`3.18.8` → `3.18.14`) and `tailscale_version`
  (`1.94.2` → `1.98.5`) to match `defaults/main.yml`.

- **Molecule (CI)**: run the alloy scenario on Debian 12 in addition to
  Ubuntu 22.04 (was Ubuntu-only), matching the two-distro coverage of the
  do and tailscale scenarios.
- **Tailscale metadata**: drop EOL Ubuntu `focal`, add `noble`, and add the `EL`
  platform (8, 9) to `galaxy_info.platforms`, matching the RedHat-family support
  already shipped in `vars/main.yml`. (Galaxy's platform enum has no Alpine/Arch
  entries, so those remain expressed via `vars/` only.)
- **Role READMEs**: link the `alloy`, `do`, and `tailscale` READMEs to the
  collection `CHANGELOG.md` so version history is discoverable from each role.
- Raise the Python target to `3.13` (the highest version `ansible-test`
  supports): bump `python_version` in `pull-request.yml` and `merge.yml` so CI
  exercises the same interpreter the release artifact is built with, matching
  `.python-version`.
- Adopt the standard Keep a Changelog header.

## [1.2.0] - 2026-03-18

### Added

- **Alloy Role** - Resource limits (`alloy_max_memory`, `alloy_max_cpu`), external labels (`alloy_external_labels`), metric allowlist filtering (`alloy_node_exporter_metric_allowlist`), journal monitoring (`alloy_enable_journal_monitoring`, `alloy_journal_config`), and new argument specs (`alloy_default_queue_config`, `alloy_service_file`)
- **DO Role** - Service config (`do_port`, `do_listen_address`, `do_storage_path`), feature flags (`do_enable_metrics`, `do_enable_logs`, `do_enable_insights`), Prometheus integration (`do_prometheus_enabled`, `do_prometheus_port`), and new argument_specs entries (`do_droplet_id`, `do_custom_config_enabled`)
- **Tailscale Role** - `tailscale_version` added to argument_specs
- **Developer Tooling** - `.ansible-lint`, security scanning configs (`.checkov.yml`, `.gitleaks.toml`, `.grype.yaml`, `.kics.json`, `.trivy.yaml`, `.secretlintrc.json`), code quality configs (`.jscpd.json`, `.markdown-link-check.json`, `.markdownlint.json`), `.pre-commit-config.yaml`, and `Makefile`

### Changed

- **Alloy Role** - Updated Grafana Alloy to v1.14.0; updated `alloy_node_exporter_config` defaults with production values; fixed argument_specs defaults for `alloy_version` and `alloy_node_exporter_config`
- **DO Role** - Translated German comments to English; fixed argument_specs default for `do_version`
- **Tailscale Role** - Improved YAML formatting for systemd override defaults
- **Developer Tooling** - Replaced `pytest.ini` with `pyproject.toml`; updated `.yamllint` and `.gitignore`; streamlined `CONTRIBUTING.md`
- **CI/CD** - Restricted Claude review to newly opened pull requests
- **Collection** - Added arillso as co-author in `galaxy.yml`
- **Dependencies** - Updated molecule-plugins to v25, pytest-cov to v7, and python dependencies

## [1.1.0] - 2026-03-08

### Changed

- **Minimum Requirements** - Bumped minimum ansible-core from 2.15 to 2.18
  - Versions 2.15, 2.16, and 2.17 are end-of-life
  - Updated `requires_ansible` in `meta/runtime.yml` to `>=2.18.0`
  - Updated `min_ansible_version` in all role metadata
  - Updated Python minimum to 3.11 (required by ansible-core 2.18)
- **CI/CD** - Migrated to reusable workflows from `arillso/.github`
  - Replaced inline CI workflow with shared `ci-ansible-collection.yml`
  - Replaced inline publish workflow with shared `release-ansible-collection.yml`
  - Added Claude Code AI review workflow
  - Added security secrets scanning workflow
  - Pinned Renovate preset to `2026-03-08` tag
- **Dependencies** - Updated development dependencies
  - Excluded `ansible-core` from Renovate updates (compatibility constraint)
  - Updated pytest, sphinx, ruff, yamllint, molecule, and other dev dependencies

## [1.0.3] - 2026-02-02

### Changed

- **Tailscale Role** - Refactored systemd service override architecture
  - Consolidated `config-override.conf.j2` and `override.conf.j2` into single unified template
  - Moved ExecStart override logic from template to [defaults/main.yml](roles/tailscale/defaults/main.yml:19-27)
  - Fixed Unit vs Service section directive handling in systemd overrides
  - Added automatic cleanup task for legacy `config-override.conf` file
  - Updated [argument_specs.yml](roles/tailscale/meta/argument_specs.yml:47-68) with detailed documentation and examples
  - Improved YAML formatting with multiline syntax for better readability

### Fixed

- **Tailscale Role** - Fixed systemd directive placement errors
  - Unit directives (After, Wants, PartOf, ReloadPropagatedFrom) now correctly placed in `[Unit]` section
  - Service directives (ExecStart, Environment, etc.) correctly placed in `[Service]` section
  - Resolves systemd warning: "Unknown key name in section 'Service'"

## [1.0.2] - 2026-02-02

### Fixed

- **Tailscale Role** - Fixed systemd service variable expansion
  - Changed PORT variable from `$PORT` to `${PORT}` in [tailscaled.service override template](roles/tailscale/templates/etc/systemd/system/tailscaled.service.d/config-override.conf.j2:8)
  - Ensures proper Bash variable expansion in systemd ExecStart directive

## [1.0.1] - 2026-01-17

### Fixed

- **Argument Specs Validation** - Fixed Galaxy publication errors by removing invalid `no_log` fields from `argument_specs.yml`
  - Removed `no_log` from alloy role (8 nested password/token fields in basic_auth and bearer_token options)
  - Removed `no_log` from do role (do_api_token field)
  - Removed `no_log` from tailscale role (tailscale_auth_key field)
  - Note: The `no_log` field is not permitted in Ansible's argument_specs schema. Sensitive values are still protected via `no_log` in task definitions.
  - Superseded (Unreleased): that note is no longer accurate. `no_log` is a valid role-arg-spec option, and it has been restored for `do_api_token`.

## [1.0.0] - 2026-01-17

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
- **Renovate** - Automated dependency updates with custom regex manager for agent version tracking (.github/renovate.json)
- **Enhanced Publish Workflow** - Improved Galaxy publishing with changelog integration

#### Molecule Tests

- **Alloy Role** - Complete molecule test suite with Docker driver
- **DO Role** - Complete molecule test suite with Docker driver
- **Tailscale Role** - Complete molecule test suite with Docker driver

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

#### Old Roles and Structure

- **Grafana Agent role** - Completely removed in favor of Grafana Alloy
- **Old DO role structure** - Replaced with modular architecture

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

- **Grafana Agent role** - Replaced by Grafana Alloy role (see Migration Guide)

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

[Unreleased]: https://github.com/arillso/ansible.agent/compare/2.0.0...HEAD
[2.0.0]: https://github.com/arillso/ansible.agent/compare/1.2.0...2.0.0
[1.2.0]: https://github.com/arillso/ansible.agent/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/arillso/ansible.agent/compare/1.0.3...1.1.0
[1.0.3]: https://github.com/arillso/ansible.agent/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/arillso/ansible.agent/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/arillso/ansible.agent/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/arillso/ansible.agent/releases/tag/1.0.0
