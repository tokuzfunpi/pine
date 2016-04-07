"""!PowerControl Functions
@package pine.powerctl
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 10:50:00
"""
from pine.cmd import os_command
import socket

def node_shutdown():
    cmds = []
    cmds.append('sudo')
    cmds.append('shutdown')
    cmds.append('-h')
    cmds.append('now')
    os_command(cmds)

def node_reboot():
    cmds = []
    cmds.append('sudo')
    cmds.append('shutdown')
    cmds.append('-r')
    cmds.append('now')
    os_command(cmds)

def node_hostname():
    return socket.gethostname()
