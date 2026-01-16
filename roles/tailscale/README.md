# Ansible Role: tailscale

Installs and configures Tailscale VPN for secure mesh networking with support for exit nodes, subnet routing, and SSH access.

## Features

- **Tailscale Installation**: Install from official repositories
- **Mesh Networking**: WireGuard-based VPN mesh topology
- **Exit Node Support**: Route internet traffic through Tailscale
- **Subnet Routing**: Access to private networks
- **SSH over Tailscale**: Secure remote access
- **Web UI and Metrics**: Management interface on port 5252
- **Multi-Distribution**: Support for Debian, Ubuntu, RHEL, Alpine, Arch

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**<https://guide.arillso.io/collections/arillso/agent/tailscale_role.html>**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.agent.tailscale
        vars:
            tailscale_auth_key: "{{ vault_tailscale_auth_key }}"
            tailscale_accept_routes: true
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
