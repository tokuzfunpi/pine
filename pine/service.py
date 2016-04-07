"""!Service Functions
@package pine.service
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 10:50:00
"""
from pine.cmd import os_command
from decorator import decorator
import psutil
import re

class AlreadyRunningError(Exception):
    '''!
    Service already running error
    '''
    def __init__(self, value=''):
        '''!Construct of exception class
        @param value error message
        '''
        self.value = value
    def __str__(self):
        return repr(self.value)

def handle_exceptions():
    '''!
    Decorator to handle all exceptions
    '''
    def wrapper(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err :
            err_msg = str(err)
            if 'job is already running' in err_msg :
                raise AlreadyRunningError(err_msg)
            elif 'already_started' in err_msg and \
                'could_not_start,rabbitmq_management' in err_msg :
                raise AlreadyRunningError(err_msg)
            raise Exception(err_msg)
    return decorator(wrapper)

@handle_exceptions()
def service_start(service):
    cmds = []
    cmds.append('sudo')
    cmds.append('service')
    cmds.append(service)
    cmds.append('start')
    res, err = os_command(cmds)
    return res, err

@handle_exceptions()
def service_restart(service):
    cmds = []
    cmds.append('sudo')
    cmds.append('service')
    cmds.append(service)
    cmds.append('restart')
    res, err = os_command(cmds)
    return res, err

@handle_exceptions()
def service_reload(service):
    cmds = []
    cmds.append('sudo')
    cmds.append('service')
    cmds.append(service)
    cmds.append('reload')
    res, err = os_command(cmds)
    return res, err

@handle_exceptions()
def service_stop(service):
    cmds = []
    cmds.append('sudo')
    cmds.append('service')
    cmds.append(service)
    cmds.append('stop')
    res, err = os_command(cmds)
    return res, err

def check_procs(process_pattern):
    cmd = 'ps -elf | grep -v grep | grep %(process_pattern)s' % \
        {'process_pattern': process_pattern}
    res, err, out=os_command(cmd, shell=True, output = True)
    validate_result(res, out, process_pattern)

def validate_result(res, result, pattern):
    _is_match = None
    if res:
        p = re.compile(pattern)
        _is_match = p.search(result)
    if _is_match is None:
        raise Exception('no such process "%(pattern)s", err_msg: %(result)s' % \
                        {'pattern': pattern, 'result' : result})

def get_process_info(p):
    try:
        cpu = int(p.get_cpu_percent(interval=0))
        rss, vms = p.get_memory_info()
        name = p.name
        pid = p.pid
    except Exception:
        name = "Closed_Process"
        pid = 0
        rss = 0
        vms = 0
        cpu = 0
    return [name.upper(), pid, rss, vms, cpu]

def get_all_process_info():
    instances = []
    all_processes = psutil.process_iter()
    for proc in all_processes:
        proc.get_cpu_percent(interval=0)
    time.sleep(1)
    for proc in all_processes:
        instances.append(get_process_info(proc))
    return instances

def get_all_process_name():
    instances = []
    all_processes = psutil.process_iter()
    for proc in all_processes:
        instances.append(proc.name.upper())
    return instances

def get_all_process_name_id():
    instances = []
    all_processes = psutil.process_iter()
    for proc in all_processes:
        nameid = [proc.name.upper(),proc.pid]
        instances.append(nameid)
    return instances

def kill_process_pid(pid):
    p = psutil.Process(pid)
    p.kill()
    return True
