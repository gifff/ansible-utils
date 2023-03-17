#!/usr/bin/python

# Copyright: (c) 2023, Gifary Dhimas Fadhillah <gifarydhimas@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: yamerge

short_description: Merge contents of YAML files

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: Merge contents of YAML files.

options:
    paths:
        description: List of paths of YAML files.
        required: true
        type: list
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name

author:
    - Gifary Dhimas Fadhillah (@gifff)
'''

EXAMPLES = r'''
# Pass in file paths
- name: Merge YAMLs
  gifff.utils.yamerge:
    name: hello world
    paths:
      - files/app-configs/production.yml
      - files/app-configs/docker-override.yml
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
content:
    description: The merge result.
    type: dict
    returned: always
    sample:
        key_a: 'hello'
'''

from ansible.module_utils.basic import AnsibleModule
import yaml

def yamerge(paths: list[str]) -> dict:
    merged_content = {}
    for filepath in paths:
        with open(filepath, 'r') as file:
            content = yaml.safe_load(file)
            if isinstance(content, dict):
                # https://stackoverflow.com/a/26853961
                # NOTE: following works for Python 3.9.0 or greater
                # merged_content |= content
                merged_content = {**merged_content, **content}
    return merged_content

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        paths=dict(type='list', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        content=dict()
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)


    try:
        result['content'] = yamerge(module.params['paths'])
        result['changed'] = True
    except FileNotFoundError as fnf_error:
        module.fail_json(msg=f'Invalid input paths. Error: {fnf_error}', **result)
    except Exception as e:
        module.fail_json(msg=f'Failed to merge YAML files. Error: {e}', **result)

    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()

