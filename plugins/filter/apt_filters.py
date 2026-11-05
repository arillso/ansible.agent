# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Arillso
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
name: apt_version_pin
version_added: "2.1.0"
short_description: Resolve an apt version pin from apt-cache madison output
description:
    - Picks the full apt version string for an upstream version out of C(apt-cache madison) output.
    - apt matches an C(=) pin against the full version string and does not expand globs in it.
      Grafana publishes C(1.21.3-1) for alloy 1.21.3, while Tailscale and DigitalOcean publish
      the bare C(1.104.4) and C(3.18.16), so the exact string has to be looked up on the host.
    - Returns C(None) when the version is not in the repository, so the calling task can fail
      with a readable message instead of a Python traceback.
options:
    _input:
        description:
            - Lines of C(apt-cache madison <package>) output, typically C(stdout_lines) of the command.
            - Each line looks like C(<package> | <version> | <repository>); only the middle field is read.
        type: list
        elements: str
        required: true
    version:
        description:
            - The upstream version to resolve, for example C(1.21.3).
            - Matched when it opens the string or follows an epoch colon, and is followed by the
              end of the string or a C(-) or C(+) separator. C(1.21.3) therefore takes C(1.21.3-1)
              but not C(1.21.30), and C(1.21) matches nothing.
            - C(~) is not a separator; in Debian ordering it sorts before the release, so
              C(1.21.3~rc.0-1) is a pre-release of 1.21.3 and never satisfies the pin.
        type: str
        required: true
author:
    - Arillso
'''

EXAMPLES = r'''
- name: Look up the versions the apt repository offers
  ansible.builtin.command:
      cmd: apt-cache madison alloy
  register: alloy_madison
  changed_when: false

- name: Resolve the full apt version string
  ansible.builtin.set_fact:
      alloy_apt_version: "{{ alloy_madison.stdout_lines | arillso.agent.apt_version_pin('1.21.3') }}"
  # Returns 1.21.3-1, or None when the repository no longer carries the version.
'''

RETURN = r'''
_value:
    description:
        - The full apt version string, epoch and revision included.
        - C(None) when no line matches the requested version.
    type: str
'''

import re

# madison prints "<pkg> | <version> | <repo>"; take the middle field.
_MADISON_LINE = re.compile(r'^[^|]*\|\s*([^|]+?)\s*\|')


def apt_version_pin(lines, version):
    """Return the full apt version string for an upstream version, or None."""
    if not lines or not version:
        return None

    wanted = re.compile(r'(^|:)' + re.escape(str(version)) + r'($|[-+])')

    for line in lines:
        match = _MADISON_LINE.match(line)
        if match and wanted.search(match.group(1)):
            return match.group(1)

    return None


class FilterModule:
    """Ansible filter module for apt version pinning."""

    def filters(self):
        return {
            'apt_version_pin': apt_version_pin,
        }
