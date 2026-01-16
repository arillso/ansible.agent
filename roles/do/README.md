# Ansible Role: do

Installs and configures the DigitalOcean Agent for automatic Droplet monitoring with zero-configuration setup.

## Features

- **DO Agent Installation**: Install from official repositories
- **Zero-Configuration**: Works automatically after installation
- **Automatic Detection**: Detects Droplet metadata via API
- **Metrics Collection**: Standard metrics without manual setup
- **Multi-Distribution**: Support for Debian, Ubuntu, RHEL, and derivatives

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**<https://guide.arillso.io/collections/arillso/agent/do_role.html>**

## Quick Start

```yaml
- hosts: digitalocean_droplets
  roles:
      - role: arillso.agent.do
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
