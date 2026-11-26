# arillso.agent

Ansible collection with three roles that install and configure host agents:
`alloy` (Grafana Alloy), `do` (DigitalOcean Agent) and `tailscale`. Published to
Ansible Galaxy as `arillso.agent`.

## Commands

`make help` lists the lint, test and build targets. Beyond those:

- One molecule scenario: `cd roles/<role> && molecule test -s <default|disabled>`.
- Combined scenario (all three roles on one host): `cd extensions && molecule test -s multi-role`.
- The alloy scenarios use the `molecule-qemu` driver and need KVM with your user
  in the `kvm` group. alloy must run as a stable systemd service, which the
  docker driver does not give. do, tailscale and multi-role use docker.

## Conventions

- **Variables are documented in `meta/argument_specs.yml` only.** The guide at
  `guide.arillso.io` renders role docs from it (antsibull-docs in `arillso/guide`),
  so role READMEs carry features and a quick start, no variable table.
- **Secret options carry `no_log: true`** in `argument_specs.yml`.
  `tests/unit/test_argument_spec_no_log.py` fails when one is missing; add new
  secret option names to its `SECRET_OPTION_NAMES`.
- **Agent versions are pinned** in `<role>_version`, in both
  `defaults/main.yml` and `meta/argument_specs.yml`, each with a
  `# renovate: datasource=… depName=…` comment on the line above. The regex
  manager in `.github/renovate.json` only bumps values that carry this comment.
- **apt pins go through the `arillso.agent.apt_version_pin` filter**
  (`plugins/filter/apt_filters.py`, called from `tasks/resolve_version.yml`).
  apt matches `=` pins against the full version string: Grafana publishes
  `1.21.3-1`, Tailscale and DigitalOcean the bare version, so the string is
  looked up on the host with `apt-cache madison`.
- **OS-specific values**: `do` uses `vars/Debian.yml` and `vars/RedHat.yml`;
  `alloy` and `tailscale` keep a per-distribution dict in `vars/main.yml`
  (`_alloy_os`, `tailscale_distributions`). Follow the pattern the role already
  uses.
- **Tasks are split by function** (`install.yml`, `configure.yml`,
  `service.yml`, `resolve_version.yml`), included from `tasks/main.yml`.
- **Changelog:** see the [Arillso organization
  guidance](https://github.com/arillso/.github/blob/main/AGENTS.md).
- **Each role ships two molecule scenarios**: `default` and `disabled`. The
  latter sets the master switch (`<role>_enabled: false`) and verifies the role
  leaves the host untouched.

## Automation

- **CI, Git hooks and reusable workflows:** see the [Arillso organization
  guidance](https://github.com/arillso/.github/blob/main/AGENTS.md) and the
  `development:repo-standard` skill.
- **Renovate** (`.github/renovate.json`): `ansible-core` and `molecule-qemu` are
  disabled on purpose. `molecule-qemu` carries its reason in the rule's
  `description`; `ansible-core` is held for compatibility (`CHANGELOG.md`, 1.1.0).

## Pitfalls

- `plugins/README.md` is Ansible's boilerplate; the real plugin lives in
  `plugins/filter/`.
- There is no `tests/integration/`: the collection ships no modules, and role
  end-to-end coverage (idempotence, distro matrix) lives in molecule.
- `do-agent` reads settings only as command-line flags. The `do` role passes
  them through a systemd drop-in; config files are not read by the agent.

## More docs

- Before a release: `CONTRIBUTING.md`, section "Release Process".
- Before reviewing a PR: `REVIEW.md` for scope and severity levels.
