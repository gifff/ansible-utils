from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.module_utils._text import to_text


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)

        result = dict(changed = False, failed = True)
        paths = self._task.args.get('paths')

        merged_content = {}

        try:
            for filepath in paths:
                content = self._loader.load_from_file(filepath)
                if isinstance(content, dict):
                    merged_content = {**merged_content, **content}
        except FileNotFoundError as fnf_error:
            result['msg'] = f'Invalid input paths. Error: {to_text(fnf_error)}'
            return result
        except Exception as e:
            result['msg'] = f'Failed to merge YAML files. Error: {to_text(e)}'
            return result


        result['failed'] = False
        result['changed'] = True
        result['content'] = merged_content
        return result

