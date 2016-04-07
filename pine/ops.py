"""!OpenStack Fucn
@package pine.ops
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 14:50:00
"""
from pine.cmd import os_command
import uuid

def virsh_screenshot(server_id, path):
    cmds = []
    cmds.append('sudo')
    cmds.append('virsh')
    cmds.append('screenshot')
    cmds.append(server_id)
    cmds.append(path)
    return os_command(cmds)

def _format_uuid_string(string):
    return (string.replace('urn:', '')
                  .replace('uuid:', '')
                  .strip('{}')
                  .replace('-', '')
                  .lower())

def is_uuid_like(val):
    """Returns validation of a value as a UUID.

    :param val: Value to verify
    :type val: string
    :returns: bool
    """
    try:
        return str(uuid.UUID(val)).replace('-', '') == _format_uuid_string(val)
    except (TypeError, ValueError, AttributeError):
        return False
