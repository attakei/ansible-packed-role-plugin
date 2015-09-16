# from ansible.plugins.callback import CallbackBase
import os
import shutil
from ansible.constants import DEFAULT_ROLES_PATH


def create_role_dir(expand_role_dir):
    """If expand_role_dir is not exist, create it.
    """
    if os.path.exists(expand_role_dir):
        return
    os.makedirs(expand_role_dir)


def expand_role(packed_role_path):
    """Create role struct folders from packed role.
    """
    expand_role_dir, _ = os.path.splitext(packed_role_path)
    create_role_dir(expand_role_dir)


class CallbackModule(object):
    CALLBACK_VERSION = 1.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'packed_role'

    def playbook_on_start(self):
        # Find roles from playbook
        all_roles = []
        for p_ in self.playbook.playbook:
            all_roles += p_['roles']
        # If there is YAML file of target role in 'roles' folder,
        # Expand to role folder all.
        packed_role_dir = os.path.join(self.playbook.basedir, 'roles')
        for role in all_roles:
            packed_role_path = os.path.join(packed_role_dir, role) + '.yml'
            if os.path.exists(packed_role_path):
                print('Found packed role: {}'.format(packed_role_path))
                expand_role(packed_role_path)
