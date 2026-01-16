# Contributing to Arillso Ansible Agent Collection

Thank you for your interest in contributing to the `arillso.agent` collection! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites

- Ansible >= 2.15
- Python >= 3.9
- Git
- A GitHub account

### Types of Contributions

We welcome various types of contributions:

- **Bug Reports:** Found a bug? Let us know!
- **Feature Requests:** Have an idea for improvement?
- **Documentation:** Improvements to docs are always appreciated
- **Code Contributions:** Bug fixes, new features, or improvements
- **Testing:** Platform testing and validation

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/ansible.agent.git
cd ansible.agent

# Add upstream remote
git remote add upstream https://github.com/arillso/ansible.agent.git
```

### 2. Install Dependencies

```bash
# Install the arillso.system collection (required for Alloy role)
ansible-galaxy collection install arillso.system

# Install development dependencies (optional)
pip install ansible-lint yamllint
```

### 3. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

## How to Contribute

### Reporting Bugs

Before creating a bug report:

1. **Search existing issues** to avoid duplicates
2. **Verify you're using a supported version** of Ansible and the collection
3. **Test on a clean environment** if possible

When filing a bug report, include:

- Collection version
- Ansible version (`ansible --version`)
- Operating system and version
- Minimal playbook to reproduce the issue
- Error messages and logs
- Steps to reproduce

Use our [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml).

### Suggesting Features

Feature requests should:

- **Align with the collection's scope** (monitoring and networking agents)
- **Provide clear use cases** and benefits
- **Consider backward compatibility**
- **Include usage examples** if possible

Use our [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml).

### Improving Documentation

Documentation improvements are highly valued:

- Fix typos, grammar, or formatting
- Add missing information or examples
- Clarify confusing sections
- Update outdated content

Use our [Documentation template](.github/ISSUE_TEMPLATE/documentation.yml).

## Coding Standards

### Ansible Best Practices

- Follow [Ansible best practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- Use FQCN (Fully Qualified Collection Names) for modules
- Properly indent YAML (2 spaces, no tabs)
- Use meaningful variable names with role prefixes (e.g., `alloy_*`, `do_*`, `tailscale_*`)

### Code Style

```yaml
# Good - Clear, descriptive, properly formatted
- name: Install Grafana Alloy package
  ansible.builtin.package:
      name: "{{ alloy_package_name }}"
      state: "{{ alloy_package_state }}"
  register: alloy_install_result
  when: alloy_enabled | bool

# Bad - Unclear, improper formatting
- name: install pkg
  package: name={{pkg}} state=present
  when: enabled
```

### Variable Naming

- Prefix with role name: `alloy_*`, `do_*`, `tailscale_*`
- Use descriptive names: `alloy_prometheus_enabled` not `alloy_prom`
- Boolean variables: Use `*_enabled`, `*_required`, etc.
- Lists: Use plural names `alloy_custom_exporters`
- Dictionaries: Use singular names `alloy_node_exporter_config`

### File Organization

Each role should follow this structure:

```
roles/ROLE_NAME/
├── defaults/
│   └── main.yml          # User-configurable variables with defaults
├── handlers/
│   └── main.yml          # Handlers for service restarts, etc.
├── meta/
│   ├── main.yml          # Role metadata
│   └── argument_specs.yml # Variable specifications and validation
├── tasks/
│   ├── main.yml          # Main entry point
│   ├── install.yml       # Package installation tasks
│   ├── configure.yml     # Configuration tasks
│   └── service.yml       # Service management tasks
├── templates/
│   └── ...               # Jinja2 templates
├── vars/
│   ├── main.yml          # Internal variables
│   ├── Debian.yml        # Debian-specific variables
│   └── RedHat.yml        # RedHat-specific variables
└── README.md             # Role documentation
```

### Documentation

All variables must be documented in three places:

1. **defaults/main.yml** - With inline comments

    ```yaml
    # Enable Prometheus metrics collection
    alloy_prometheus_enabled: false
    ```

2. **meta/argument_specs.yml** - With full specifications

    ```yaml
    alloy_prometheus_enabled:
        type: "bool"
        required: false
        default: false
        description: "Enable Prometheus metrics collection and remote write"
    ```

3. **README.md** - With usage examples

    ````markdown
    ### Prometheus Configuration

    ```yaml
    alloy_prometheus_enabled: true
    alloy_prometheus_remote_write_url: "https://prometheus.example.com/api/v1/write"
    ```
    ````

## Testing Requirements

### Before Submitting

1. **Lint your code:**

    ```bash
    ansible-lint roles/ROLE_NAME/
    yamllint roles/ROLE_NAME/
    ```

2. **Test on supported platforms:**
    - At minimum, test on one major platform (Ubuntu, Debian, or RHEL)
    - Ideally, test on multiple platforms

3. **Verify the collection builds:**

    ```bash
    ansible-galaxy collection build --force
    ansible-galaxy collection install arillso-agent-*.tar.gz --force
    ```

4. **Test with a minimal playbook:**

    ```yaml
    ---
    - name: Test role
      hosts: localhost
      become: true
      roles:
          - role: arillso.agent.ROLE_NAME
            vars:
                # Minimal configuration
    ```

### Manual Testing

Create a test playbook and verify:

- Role installs without errors
- Service starts and runs correctly
- Configuration files are created properly
- No regressions in existing functionality
- Idempotency (running twice doesn't change anything)

## Pull Request Process

### 1. Prepare Your Changes

```bash
# Ensure you're up to date with upstream
git fetch upstream
git rebase upstream/main

# Run tests
ansible-lint roles/ROLE_NAME/

# Build collection
ansible-galaxy collection build --force
```

### 2. Commit Guidelines

Write clear, descriptive commit messages:

```
Add Faro configuration to Alloy role

- Add alloy_enable_faro variable to defaults
- Add Faro receiver configuration to templates
- Update README with Faro examples
- Add argument_specs for Faro variables

Fixes #123
```

Format:

- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description with bullet points
- Reference related issues

### 3. Create Pull Request

1. Push your branch to your fork
2. Create a PR using our [PR template](.github/pull_request_template.md)
3. Fill out all sections of the template
4. Link related issues
5. Mark as draft if work in progress

### 4. PR Review Process

- **Maintainer review** - A maintainer will review your PR
- **Feedback** - Address any requested changes
- **CI checks** - Ensure all automated checks pass
- **Testing** - Provide test results
- **Approval** - At least one maintainer approval required
- **Merge** - Maintainer will merge when ready

### 5. After Merge

- Delete your feature branch
- Update your fork's main branch
- Celebrate! 🎉

## Documentation

### README Updates

When adding features or changing behavior:

- Update the relevant role's README.md
- Add usage examples
- Update the requirements section if needed
- Add troubleshooting notes if applicable

### Changelog

For significant changes:

- Add an entry to `CHANGELOG.md` under the `[Unreleased]` section
- Follow the [Keep a Changelog](https://keepachangelog.com/) format
- Categorize as Added, Changed, Deprecated, Removed, Fixed, or Security

Example:

```markdown
## [Unreleased]

### Added

- Faro receiver support in Alloy role (#123)
```

### Comments

- Document complex logic
- Explain non-obvious decisions
- Reference issues or documentation
- Keep comments up-to-date with code changes

## Community

### Getting Help

- **Issues:** Use GitHub issues for bugs and feature requests
- **Discussions:** For questions and general discussion
- **Documentation:** Check the README files first

### Communication

- Be respectful and constructive
- Follow the Code of Conduct
- Provide context and details
- Be patient - maintainers are volunteers

### Recognition

Contributors are recognized in:

- CHANGELOG.md for their contributions
- GitHub contributors page
- Release notes

## Version Compatibility

- **Ansible:** >= 2.15
- **Python:** >= 3.9
- **Platforms:**
    - Ubuntu 20.04, 22.04, 24.04
    - Debian 11, 12
    - RHEL/CentOS 8, 9
    - Alpine Linux (Tailscale only)
    - Arch Linux (Tailscale only)

## Questions?

If you have questions about contributing:

1. Check existing documentation
2. Search closed issues
3. Open a new discussion on GitHub
4. Tag maintainers if needed

---

**Thank you for contributing to arillso.agent!**

Your contributions help make this collection better for everyone.
