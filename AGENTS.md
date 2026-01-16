# Ansible Collection: arillso.agent

## Context

This is an Ansible collection that provides production-ready roles for deploying and configuring monitoring, observability, and networking agents. The collection includes Grafana Alloy for comprehensive observability, DigitalOcean Agent for Droplet monitoring, and Tailscale for secure mesh VPN networking.

## Structure

### Collection Structure

```text
ansible.agent/
├── .github/workflows/
│   ├── ci.yml              # All-in-one: linting, tests, build
│   └── publish.yml         # Galaxy publishing
├── roles/
│   ├── alloy/             # Grafana Alloy observability agent
│   ├── do/                # DigitalOcean monitoring agent
│   └── tailscale/         # Tailscale VPN mesh network
├── tests/
│   ├── integration/       # Integration tests (ansible-test)
│   └── unit/             # Unit tests (pytest)
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── galaxy.yml
├── pytest.ini
└── requirements.txt
```

### Role Structure

Each role follows standard Ansible role structure:

- `tasks/` - Main task files organized by function (install.yml, configure.yml, service.yml)
- `defaults/` - Default variables (minimal comments, examples in comments)
- `vars/` - OS-specific variables (Debian.yml, RedHat.yml)
- `handlers/` - Handlers for service restarts
- `templates/` - Jinja2 templates for configuration files
- `meta/` - Role metadata with `argument_specs.yml` (required)

### Roles

- **alloy** - Grafana Alloy for metrics, logs, and traces collection
- **do** - DigitalOcean Agent for Droplet monitoring
- **tailscale** - Tailscale VPN for secure mesh networking

## Conventions

### Code Style

- Use 4 spaces for indentation in YAML files
- Follow Ansible best practices and naming conventions
- Use descriptive variable names with role prefixes
- Minimal comments in defaults/main.yml (keep it clean)
- Examples in comments for complex variables
- Use handlers for service management
- Organize tasks by function (install, configure, service)

### Testing

Three-level testing strategy:

1. **Unit Tests** (pytest) - For plugins
    - Location: `tests/unit/`
    - Run: `pytest tests/unit/`

2. **Molecule Tests** - For individual roles (optional)
    - Location: `roles/*/molecule/default/`
    - Run: `molecule test -s default`

3. **Integration Tests** (ansible-test) - For role integration
    - Location: `tests/integration/targets/`
    - Run: `ansible-test integration`

All tests consolidated in single `ci.yml` workflow.

### Documentation

**Keep documentation DRY:**

1. **Collection README** - Overview + all roles listed with features
2. **Role README** - Features + Quick Start + link to guide (if available)
3. **argument_specs.yml** - Complete variable documentation
4. **CONTRIBUTING.md** - Development guidelines and standards

## Workflows

### CI/CD

**Standard workflows:**

- `ci.yml` - All linting, tests (unit, integration), and build
- `publish.yml` - Galaxy publishing (triggered by tag)

### Release Process

**IMPORTANT: Always update CHANGELOG.md before releasing!**

1. **Update CHANGELOG.md** (REQUIRED)
    - Move items from `## [Unreleased]` to new version section
    - Document all changes under appropriate sections (Added, Changed, Fixed, etc.)

2. **Update galaxy.yml version**
    - Use semantic versioning (MAJOR.MINOR.PATCH)
    - Example: `version: "1.0.1"`

3. **Create and push git tag**
    - Use version **without 'v' prefix** (e.g., `1.0.1` not `v1.0.1`)
    - Command: `git tag 1.0.1 && git push origin 1.0.1`

4. **Automated workflow triggers**
    - `publish.yml` publishes to Ansible Galaxy
    - Creates GitHub Release with CHANGELOG notes

## Do

- ✅ Always use argument_specs.yml for all roles
- ✅ Keep defaults/main.yml clean (minimal comments)
- ✅ Test with ansible-lint before committing
- ✅ Update CHANGELOG.md before releasing
- ✅ Use MIT license with copyright years 2022-2026
- ✅ Organize tasks by function (install, configure, service)
- ✅ Use OS-specific variables in vars/ directory

## Do Not

- ❌ Do not commit secrets or sensitive data
- ❌ Do not create roles without argument_specs.yml
- ❌ Do not use deprecated Ansible syntax
- ❌ Do not hardcode values that should be variables
- ❌ Do not add excessive comments to defaults/main.yml
- ❌ Do not create separate test workflows (use ci.yml)
- ❌ Do not skip CHANGELOG.md updates before releases
- ❌ Do not use 'v' prefix in Ansible Collection tags
