# ansible_apply_role

Apply particular Ansible role(s) to host(s)

## Installation

```
pip install ansible-apply-role
```

## Usage

```
usage: ansible_apply_role [-h] --hostpattern HOSTPATTERN
                          --roles ROLES [ROLES ...]
                          [--gather_facts GATHER_FACTS]
                          [--ansible_playbook_args ANSIBLE_PLAYBOOK_ARGS [ANSIBLE_PLAYBOOK_ARGS ...]]
                          [--show-playbook]
                          [--tempfile-directory TEMPFILE_DIRECTORY]

options:
  -h, --help            show this help message and exit
  --hostpattern HOSTPATTERN
                        Ansible host pattern
  --roles ROLES [ROLES ...]
                        List of roles to apply
  --gather_facts GATHER_FACTS
                        Enable or disable gathering of ansible facts before
                        applying roles (default: False)
  --ansible_playbook_args ANSIBLE_PLAYBOOK_ARGS [ANSIBLE_PLAYBOOK_ARGS ...]
                        Additional argument to pass on to 'ansible-playbook'
                        executable (default: [])
  --show-playbook       Print resulting playbook and exit (default: False)
  --tempfile-directory TEMPFILE_DIRECTORY
                        Directory in which temporary playbook will be created
                        (default: $PWD)
```

### Example

```
ansible_apply_role \
  --hostpattern lb-west.example.com \
  --roles test \
  --ansible_playbook_args="--check"
```
