# Ansible Collection: arillso.agent

## Context

This is an Ansible collection that provides production-ready roles for deploying and configuring monitoring, observability, and networking agents. The collection includes Grafana Alloy for comprehensive observability, DigitalOcean Agent for Droplet monitoring, and Tailscale for secure mesh VPN networking.

## Structure

### Collection Structure

```text
ansible.agent/
├── .github/workflows/
│   ├── pull-request.yml    # Lint, tests, secret scan, Claude review on PRs
│   ├── merge.yml           # CI + secret scan on push to main
│   ├── nightly-security.yml # Scheduled daily secret scan
│   └── tag.yml             # Galaxy publishing (triggered by tag)
├── roles/
│   ├── alloy/             # Grafana Alloy observability agent
│   ├── do/                # DigitalOcean monitoring agent
│   └── tailscale/         # Tailscale VPN mesh network
├── extensions/molecule/
│   └── multi-role/        # Combined molecule scenario (all three roles)
├── tests/
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

Two-level testing strategy:

1. **Unit Tests** (pytest) - For templates and role metadata
   - Location: `tests/unit/`
   - Run: `pytest tests/unit/`

2. **Molecule Tests** - Role end-to-end, per-role and combined
   - Per-role location: `roles/*/molecule/{default,disabled}/`
   - Combined location: `extensions/molecule/multi-role/` (deploys alloy, do
     and tailscale together on one host)
   - Run: `molecule test -s default` (per role) / `molecule test -s multi-role`
   - CI: one `molecule-<role>` job per role plus `molecule-multi-role` in `pull-request.yml`

There is no `tests/integration/` (`ansible-test integration`): that level targets
modules and plugins, and this collection ships none (`plugins/` holds only a
README). Role end-to-end coverage belongs in molecule, which also gives the
idempotence check and the multi-distro matrix that `ansible-test` would not.

Tests run via the reusable CI (`arillso/.github`) on pull requests and merges.

### Documentation

**Keep documentation DRY:**

1. **Collection README** - Overview + all roles listed with features
2. **Role README** - Features + Quick Start + link to guide (if available)
3. **argument_specs.yml** - Complete variable documentation
4. **CONTRIBUTING.md** - Development guidelines and standards

## Workflows

### CI/CD

Event-focused workflows calling reusables from `arillso/.github`:

- `pull-request.yml` - Lint, unit tests, per-role molecule, secret scan, and Claude review on PRs
- `merge.yml` - Same CI plus secret scan on push to `main`
- `nightly-security.yml` - Scheduled daily secret scan
- `tag.yml` - Publishes to Ansible Galaxy on tag push (e.g. `1.0.1`)

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
   - `tag.yml` publishes to Ansible Galaxy
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
- ❌ Do not create separate test workflows (CI runs via the reusable in `pull-request.yml`/`merge.yml`)
- ❌ Do not skip CHANGELOG.md updates before releases
- ❌ Do not use 'v' prefix in Ansible Collection tags
