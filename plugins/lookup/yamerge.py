from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
  name: yamerge
  author: Gifary Dhimas Fadhillah (@gifff) <gifarydhimas@gmail.com>
  version_added: "1.2.0"  # for collections, use the collection version, not the Ansible version
  short_description: read merged YAML files contents
  description:
      - This lookup returns the contents from merged YAML files on the Ansible controller's file system.
  options:
    _terms:
      description: path(s) of YAML files to read
      required: True
  notes:
    - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
    - this lookup does not understand globbing --- use the fileglob lookup instead.
"""
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

      self.set_options(var_options=variables, direct=kwargs)

      merged_content = {}
      for term in terms:
          display.debug("Yamerge lookup term: %s" % term)

          # Find the file in the expected search path
          lookupfile = self.find_file_in_search_path(variables, 'files', term)
          display.vvvv(u"Yamerge lookup using %s as file" % lookupfile)
          try:
              if lookupfile:
                  content = self._loader.load_from_file(lookupfile)
                  if isinstance(content, dict):
                      merged_content = {**merged_content, **content}
                  else:
                      raise AnsibleParserError('Invalid YAML/JSON file "%s" ' % term)
              else:
                  raise AnsibleParserError('Unable to find file matching "%s" ' % term)
          except AnsibleParserError:
              raise AnsibleError("could not locate file in lookup: %s" % term)

      return [merged_content]

