# Ansible Collection: arillso.agent

[![License](https://img.shields.io/github/license/arillso/ansible.agent?style=popout-square)](LICENSE)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-arillso.agent-blue.svg?style=popout-square)](https://galaxy.ansible.com/arillso/agent)
[![CI](https://img.shields.io/github/actions/workflow/status/arillso/ansible.agent/merge.yml?branch=main&style=popout-square&label=ci)](https://github.com/arillso/ansible.agent/actions/workflows/merge.yml)

Ansible roles that install and configure monitoring, observability and
networking agents on Linux hosts.

## Roles

- **[alloy](roles/alloy/README.md)**: Grafana Alloy for metrics, logs and
  traces, with Node Exporter and OpenTelemetry support
- **[do](roles/do/README.md)**: DigitalOcean Agent for Droplet monitoring
- **[tailscale](roles/tailscale/README.md)**: Tailscale mesh VPN with exit
  nodes and subnet routing

## Installation

```bash
ansible-galaxy collection install arillso.agent
```

Or in `requirements.yml`:

```yaml
---
collections:
  - name: arillso.agent
    version: ">=2.0.0"
```

## Quickstart

```yaml
---
- name: Install agents
  hosts: servers
  become: true
  roles:
    - role: arillso.agent.alloy
      vars:
        alloy_prometheus_enabled: true
        alloy_loki_enabled: true
    - role: arillso.agent.do
    - role: arillso.agent.tailscale
      vars:
        tailscale_auth_key: "{{ vault_tailscale_auth_key }}"
```

Each role has an `<role>_enabled` switch; set it to `false` to skip the role on
a host.

## Configuration

Every role variable is described in the role's `meta/argument_specs.yml`. The
rendered reference with examples is in the
[guide](https://guide.arillso.io/collections/arillso/agent/).

## Requirements

- ansible-core >= 2.18
- systemd on the target hosts
- the `arillso.system` collection (installed as a dependency)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, tests and the release process.

## License

MIT, see [LICENSE](LICENSE).

(c) 2022-2026, Arillso
