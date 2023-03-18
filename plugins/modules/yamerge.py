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

