# Contributing to arillso.agent

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Prerequisites

- Ansible >= 2.18
- Python >= 3.12
- Git
- Docker (for testing)

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/ansible.agent.git
cd ansible.agent
git remote add upstream https://github.com/arillso/ansible.agent.git
```

### 2. Install Dependencies

```bash
make install-dev
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

## Coding Standards

### YAML

- Use 4 spaces for indentation (no tabs)
- Use lowercase with underscores for variable names
- Prefix role variables with the role name
- Keep lines under 500 characters
- Require `---` document start

### Python

- Follow PEP 8 style guidelines
- Use 4 spaces for indentation
- Line length: 100 characters (enforced by black/ruff)
- Add docstrings for functions and classes

### Ansible Best Practices

- **Idempotency**: All tasks must be idempotent
- **Handlers**: Use handlers for service restarts and reloads
- **FQCN**: Use Fully Qualified Collection Names for modules
- **Variables**: Document all variables in `meta/argument_specs.yml`
- **Argument Specs**: Always provide `meta/argument_specs.yml`
- **Tags**: Use meaningful tags for task organization

### Role Structure

```text
roles/ROLE_NAME/
├── defaults/
│   └── main.yml              # User-configurable variables
├── handlers/
│   └── main.yml              # Service handlers
├── meta/
│   ├── main.yml              # Role metadata
│   └── argument_specs.yml    # Variable specifications
├── tasks/
│   ├── main.yml              # Main entry point
│   ├── install.yml           # Installation tasks
│   ├── configure.yml         # Configuration tasks
│   └── service.yml           # Service management
├── templates/                # Jinja2 templates
├── vars/                     # OS-specific values: Debian.yml/RedHat.yml (do)
│   └── main.yml              # or a per-distribution dict (alloy, tailscale)
└── README.md                 # Role documentation
```

## Testing

### Linting

```bash
make lint
```

This runs ansible-lint, yamllint, and Python linters (ruff, black).

### Unit Tests

```bash
make test-unit
```

### Molecule Tests

```bash
make test-molecule
```

This runs every molecule scenario serially and stops at the first failure.
The alloy scenarios use the qemu driver, so they need KVM and your user in the
`kvm` group.

### Auto-format

```bash
make format
```

### Build Collection

```bash
make build
```

## Submitting Changes

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/), scoped to
the role when the change touches one:

```text
<type>(<scope>): <summary in imperative mood>

Optional body explaining what changed and why.

Fixes #123
```

- `type`: `feat`, `fix`, `docs`, `test`, `ci`, `refactor`, `chore`
- `scope`: the role (`alloy`, `do`, `tailscale`), `deps` for dependency
  updates, `molecule` for test scenarios, `repo` for repository tooling;
  omit it when no scope fits
- Example: `fix(tailscale): fix RHEL repo, auth key exposure and service handling`

The pull request title follows the same format.

### Pull Request Process

1. Ensure your branch is up to date with `main`
2. Run `make lint` and fix all issues
3. Update `CHANGELOG.md` under `[Unreleased]`
4. Update relevant documentation
5. Create PR using our [PR template](.github/pull_request_template.md)
6. Fill out all template sections and link related issues

### PR Review

- A maintainer will review your PR
- Address any requested changes
- All CI checks must pass
- At least one maintainer approval required

## Release Process

**Note**: Only maintainers can create releases.

1. Update `CHANGELOG.md` - move items from `[Unreleased]` to new version
2. Update `galaxy.yml` version (semantic versioning)
3. Create and push tag (without `v` prefix):

```bash
git tag 1.0.1
git push origin 1.0.1
```

GitHub Actions automatically publishes to Ansible Galaxy and creates a GitHub Release.

## Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Templates**: Use our issue templates for structured reports

---

**Thank you for contributing!**
