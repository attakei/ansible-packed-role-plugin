Ansible packed-role plugin
==========================

What is this?
-------------

This is callback plugin for ansible. I generate file set structured as role from role packaging YAML file.


Usage example
-------------

#. Get packed_role.py and set callback plugins directory.
#. Edit your ansible.cfg to use user callback plugin.
#. Create your role as one yaml file.
#. Run playbook.

Current issues
--------------

- Plugin can run only 1.9.x. not run devel(>=2.0.0 ?)
- Plugin generate role directory into same path with role YAML. I think that it must generate other roles path directory.

License
-------

See `LICENSE <./LICENSE>`_
