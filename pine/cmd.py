"""!Cmd Functions
@package pine.cmd
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 10:50:00
"""
import commands
import shlex
import datetime
import subprocess
import signal
import time
import os

def run_simple_cmd(cmd):
    return commands.getoutput(cmd)

def run_cmd(cmd, check_ret=True, retry=2, accept_retcode=[0]):
    while check_ret:
        ret, res = commands.getstatusoutput(cmd)
        if ret > 0:
            if retry == 0 :
                return None, None
            else:
                retry -= 1
                time.sleep(1)
        else:
            break
    if not check_ret:
        ret, res = commands.getstatusoutput(cmd)
    return ret, res

def run_cmd_to(cmd, check_ret=True, timeout=3):
    command = shlex.split(cmd)
    start = datetime.datetime.now()
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    while process.poll() is None:
      time.sleep(0.1)
      now = datetime.datetime.now()
      if (now - start).seconds> timeout:
        os.kill(process.pid, signal.SIGKILL)
        os.waitpid(-1, os.WNOHANG)
        return None, None
    return process.returncode, process.communicate()

def os_command(cmds, shell=False, output=False, executable=None):
    proc = subprocess.Popen(cmds, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=shell, executable=executable)
    out, err = proc.communicate()
    if proc.returncode:
        res = False
    else:
        res = True
    if output :
        return (res, err, out)
    else :
        return (res, err)

def execute(cmd, root= True, status=False, check=False):
    if check :
        if root :
            _s, _msg = commands.getstatusoutput('sudo {0}'.format(cmd))
        else :
            _s, _msg = commands.getstatusoutput(cmd)
        if _s :
            raise Exception(_msg)
        else :
            return True
    if status:
        if root:
            return commands.getstatusoutput('sudo {0}'.format(cmd))
        else:
            return commands.getstatusoutput(cmd)
    if not root:
        return commands.getoutput(cmd)
    return commands.getoutput('sudo {0}'.format(cmd))
