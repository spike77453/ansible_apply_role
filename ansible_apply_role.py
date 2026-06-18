#!/usr/bin/env python3

import argparse
import sys
import tempfile
import os
import pty

from jinja2 import BaseLoader, Environment


def _parse_args() -> argparse.Namespace:
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="ansible_apply_role",
    )
    argparser.add_argument(
        "--hostpattern",
        help="Ansible host pattern",
        required=True,
    )
    argparser.add_argument(
        "--roles",
        action="extend",
        help="List of roles to apply",
        nargs="+",
        required=True,
        type=str,
    )
    argparser.add_argument(
        "--gather_facts",
        default=False,
        help="Enable or disable gathering of ansible facts before applying roles",
        type=bool,
    )
    argparser.add_argument(
        "--ansible_playbook_args",
        action="extend",
        default=[],
        help="Additional argument to pass on to 'ansible-playbook' executable",
        nargs="+",
        type=str,
    )
    argparser.add_argument(
        "--show-playbook",
        action="store_true",
        help="Print resulting playbook and exit",
        required=False,
    )
    argparser.add_argument(
        "--tempfile-directory",
        help="Directory in which temporary playbook will be created",
        default=os.getcwd(),
    )
    args = argparser.parse_args()
    return args


PLAYBOOK_TEMPLATE = """
- hosts: {{ hostpattern }}
  gather_facts: {{ gather_facts }}
  roles:
{%- for role in roles %}
    - {{ role }}
{%- endfor %}

"""


def main() -> int:
    args = _parse_args()

    template = Environment(loader=BaseLoader()).from_string(PLAYBOOK_TEMPLATE)
    rendered_template = template.render(
        hostpattern=args.hostpattern, roles=args.roles, gather_facts=args.gather_facts
    )

    if args.show_playbook:
        print(rendered_template)
        return 0

    with tempfile.NamedTemporaryFile(
        mode="w", dir=args.tempfile_directory, suffix=".yml"
    ) as tmp_file:
        tmp_file.write(rendered_template)
        tmp_file.flush()
        cmd = ["ansible-playbook", tmp_file.name] + args.ansible_playbook_args
        print(f"Executing command: {' '.join(cmd)}")
        return pty.spawn(cmd, lambda fd: os.read(fd, 1024))


if __name__ == "__main__":
    sys.exit(main())
