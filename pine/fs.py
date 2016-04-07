"""!FileSystem Functions
@package pine.fs
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 10:50:00
"""
from pine.cmd import os_command, run_cmd
import os

def get_file_name(path):
    return path.split('/')[-1]

def touch_file(path):
    with open(path, 'a'):
        os.utime(path, None)

def remove_file(path, root=True):
    cmds = []
    if root :
        cmds.append('sudo')
    cmds.append('rm')
    cmds.append(path)
    return os_command(cmds)

def copy_file(from_path, to_path, multi=False, root=True, shell=False):
    cmds = []
    if root :
        cmds.append('sudo')
    cmds.append('cp')
    if multi :
        cmds.append('-rf')
    cmds.append(from_path)
    cmds.append(to_path)
    if shell:
        cmds = ' '.join(cmds)
    return os_command(cmds, shell=shell)

def remove_folder(path, root=True):
    empty_flag = False
    if path.endswith('/*') :
        _path = dirname(path)
        empty_flag = True
    else :
        _path = path
    cmds = []
    if root :
        cmds.append('sudo')
    cmds.append('rm')
    cmds.append('-rf')
    cmds.append(_path)
    res, err = os_command(cmds)
    if empty_flag :
        create_folder(_path)
    return res, err

def move_file(from_path, to_path, root=True):
    cmds = []
    if root :
        cmds.append('sudo')
    cmds.append('mv')
    cmds.append(from_path)
    cmds.append(to_path)
    return os_command(cmds)

def isfile(path):
    return os.path.isfile(path)

def isdir(path):
    return os.path.isdir(path)

def dirname(path):
    return os.path.dirname(path)

def list_dir(path):
    return os.listdir(path)

def path_join(*args):
    return os.path.join(*args)

def abs_path(path):
    return os.path.abspath(path)

def create_folder(path):
    os.makedirs(path)

def chmod(path, mode):
    cmds = 'chmod {0} {1}'.format(mode, path)
    cmds_list = cmds.split(' ')
    return os_command(cmds_list)

def chown(path, mode):
    cmds = 'chown -R {0} {1}'.format(mode, path)
    cmds_list = cmds.split(' ')
    return os_command(cmds_list)

def path_exists(path):
    if not os.path.exists(path):
        return False
    return True

def check_dir_empty(path):
    #empty return True
    list_dir = os.listdir(path)
    if len(list_dir):
        return False
    else:
        return True

def fsync(fd):
    os.fsync(fd)

def write_file(file_path, data):
    with open(file_path, 'wb') as fd:
        fd.write(data)
        fsync(fd)

def read_file(file_path):
    data = ''
    with open(file_path, 'r') as fd:
        data = fd.read()
    return data

def chunkiter(fp, chunk_size=65536):
    while True:
        chunk = fp.read(chunk_size)
        if chunk:
            yield chunk
        else:
            break

def chunkreadable(iter, chunk_size=65536):
    return chunkiter(iter, chunk_size) if hasattr(iter, 'read') else iter

def untar(path, target_path, verbose=False):
    '''
    @param path untar file path
    @param target_path untar result path
    '''
    cmd = ['tar']
    if verbose:
        cmd.append('-zxvf {0}'.format(path))
    else:
        cmd.append('-zxf {0}'.format(path))
    cmd.append('-C {0}'.format(target_path))
    cmd = ' '.join(cmd)
    return run_cmd(cmd)
