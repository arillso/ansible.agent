# Ansible Role: alloy

Installs and configures Grafana Alloy for monitoring and observability with support for Prometheus, Loki, OpenTelemetry, and custom exporters.

## Features

- **Grafana Alloy Installation**: Install from official repositories
- **Prometheus Metrics**: Collection with Node Exporter integration
- **Loki Log Collection**: File and systemd journal sources
- **OpenTelemetry Support**: OTLP receiver and exporters
- **Custom Exporters**: Tailscale metrics integration
- **Advanced Relabeling**: Dedicated prometheus.relabel components
- **Multi-Distribution**: Support for Debian, Ubuntu, RHEL, and derivatives

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**<https://guide.arillso.io/collections/arillso/agent/alloy_role.html>**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.agent.alloy
        vars:
            alloy_prometheus_enabled: true
            alloy_node_exporter_enabled: true
            alloy_loki_enabled: true
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
