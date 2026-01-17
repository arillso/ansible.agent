# Ansible Collection: arillso.agent

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=popout-square)](LICENSE) [![Ansible Galaxy](http://img.shields.io/badge/ansible--galaxy-arillso.agent-blue.svg?style=popout-square)](https://galaxy.ansible.com/arillso/agent)

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

This project is under the MIT License. See the [LICENSE](LICENSE) file for the full license text.

## Copyright

(c) 2022-2026, Arillso
