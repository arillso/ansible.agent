# Ansible Collection: arillso.agent

[![CI](https://github.com/arillso/ansible.agent/workflows/CI/badge.svg)](https://github.com/arillso/ansible.agent/actions)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-arillso.agent-blue.svg)](https://galaxy.ansible.com/arillso/agent)
[![License](https://img.shields.io/github/license/arillso/ansible.agent)](LICENSE)

## Description

This Ansible collection provides production-ready roles for deploying and
configuring monitoring, observability, and networking agents across Linux
infrastructure.

## Roles

- **[alloy](roles/alloy/README.md)** - Grafana Alloy for metrics, logs, and
  traces collection with Node Exporter and OpenTelemetry support
- **[do](roles/do/README.md)** - DigitalOcean Agent for automatic Droplet
  monitoring with zero-configuration setup
- **[tailscale](roles/tailscale/README.md)** - Tailscale VPN for secure mesh
  networking with exit nodes and subnet routing

## Installation

Install this collection from Ansible Galaxy:

```bash
ansible-galaxy collection install arillso.agent
```

Or add it to your `requirements.yml`:

```yaml
---
collections:
    - name: arillso.agent
      version: ">=1.0.0"
```

## Requirements

- Ansible >= 2.15
- systemd on target systems

## Dependencies

This collection depends on `arillso.system` for package management:

```bash
ansible-galaxy collection install arillso.system
```

## Documentation

Full documentation is available at:
<https://guide.arillso.io/collections/arillso/agent/>

## License

<!-- markdownlint-disable -->

This project is under the MIT License. See the [LICENSE](LICENSE) file for the full license text.

<!-- markdownlint-enable -->

## Copyright

(c) 2022-2026, Arillso
