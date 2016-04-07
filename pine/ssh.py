"""!SSH Func
@package pine.ssh
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 15:00:00
"""
from pine.cmd import execute
from pine.utils import sleep

def ssh_copy_from(host, source, destination, user="root"):
    cmd = "scp {user}@{host}:{source} {destination}".format(
        user=user, host=host, source=source, destination=destination)
    sleep(1)
    return execute(cmd, status=True)

def ssh_copy_to(host, source, destination, user="root"):
    cmd = "scp {source} {user}@{host}:{destination}".format(
        user=user, host=host, source=source, destination=destination)
    sleep(1)
    return execute(cmd, status=True)
