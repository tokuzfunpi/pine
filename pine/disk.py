"""!Disk Functions
@package pine.hw
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 10:50:00
"""
from pine.cmd import os_command
from tempfile import mkstemp
import commands
import subprocess
import shutil
import os
from pine.fs import path_exists

def is_mount(path):
    if path_exists(path):
        return os.path.ismount(path)
    else:
        return False

def get_disks():
    disks = []
    _disks = []
    cmd = "sudo fdisk -l 2>/dev/null | egrep -o '(/dev/[^:]*):'" + \
          " | awk -F: '{print $1}'"
    result, err, output = os_command(cmd, True, True)
    if result :
        output = output.strip()
        _disks = output.split()
    bulks = get_bulks()
    for disk in _disks :
        _check = False
        for bulk in bulks :
            if disk in bulk['name'] :
                _check = True
                break
        if 'mapper' in disk : continue
        if not _check :
            dev_name = disk + '1'
            mount_path = get_mount_path()
            partition_system(disk)
            format_xfs(dev_name)
            mount_part(dev_name, mount_path)
            _bulks = get_bulks()
            uuid = None
            for bulk in _bulks :
                if bulk['name'] == dev_name : 
                    uuid = bulk['uuid']
            append_fstab(uuid, mount_path)
        disks.append(disk)
    return disks

def auto_format_disks():
    disks = []
    cmd = "sudo fdisk -l 2>/dev/null | egrep -o '(/dev/[^:]*):'" + \
          " | awk -F: '{print $1}'"
    result, err, output = os_command(cmd, True, True)
    if result :
        output = output.strip()
        disks = output.split()
    bulks = get_bulks()
    for disk in disks :
        _check = False
        for bulk in bulks :
            if disk in bulk['name'] :
                _check = True
                break
        if 'mapper' in disk : continue
        if not _check :
            dev_name = disk + '1'
            mount_path = get_mount_path()
            partition_system(disk)
            format_xfs(dev_name)
            mount_part(dev_name, mount_path)
            _bulks = get_bulks()
            uuid = None
            for bulk in _bulks :
                if bulk['name'] == dev_name : 
                    uuid = bulk['uuid']
            append_fstab(uuid, mount_path)

def append_fstab(uuid, mount_path) :
    cmd = "UUID={0} {1} xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0\n"
    with open("/etc/fstab", "a") as fd:
        fd.write(cmd.format(uuid, mount_path))

def get_device_path(mount_path):
    cmd = "sudo mount | grep \"{0} \"".format(mount_path)
    cmd = cmd + "| awk '{print $1}'"
    result, err, output = os_command(cmd, True, True)
    if result :
        output = output.strip()
        return output.split()[0]
    else :
        raise OSError('Can\'t find device')

def remove_part_in_fstab(uuid, file_path='/etc/fstab'):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path, 'w')
    old_file = open(file_path, 'r')
    for line in old_file:
        if uuid not in line :
            new_file.write(line)
    #close temp file
    new_file.close()
    os.close(fh)
    old_file.close()
    #Remove original file
    os.remove(file_path)
    #Move new file
    shutil.move(abs_path, file_path)

def get_mount_path():
    i = 1
    path = '/mnt/disk1'
    while True :
        if not os.path.exists('/mnt/disk' + str(i)):
            path = '/mnt/disk' + str(i)
            break
        else :
            i += 1
    return path

def partition_system(dev):
    cmd = 'parted -s {0} mklabel gpt mkpart primary 0% 100%'.format(dev)
    run_cmd(cmd)

def remove_partition(dev):
    cmd = 'parted {0} rm 1'.format(dev)
    run_cmd(cmd)

def format_xfs(part):
    cmd = 'mkfs.xfs {0}'.format(part)
    run_cmd(cmd)

def mount_part(part, mpoint):
    if not os.path.exists(mpoint):
        os.mkdir(mpoint)
    _cmd = 'mount -t xfs -o nodiratime,noatime,nobarrier,logbufs=8 {0} {1}'
    cmd = _cmd.format(part, mpoint)
    run_cmd(cmd)

def unmount_part(mpoint):
    if not os.path.exists(mpoint):
        return
    run_cmd('sudo umount {0}'.format(mpoint))
    run_cmd('sudo rm -rf {0}'.format(mpoint))

def unmount(path):
    run_cmd('sudo umount {0}'.format(path))

def get_bulks():
    cmd = "sudo blkid "
    result, err, output = os_command(cmd, True, True)
    disks = []
    output =  output.strip().split('\n')
    for l in output :
        _l = l.strip().split(' ')
        dev_name = _l[0][:-1]
        uuid = _l[1].split('"')[1]
        dev_type = _l[2].split('"')[1]
        if 'mapper' in dev_name : continue
        if dev_type in ['swap', 'LVM2_member'] : continue
        disk = {
            'name' : dev_name,
            'uuid' : uuid,
            'format' : dev_type
        }
        disks.append(disk)
    return disks

def get_disk_infos(all=False):
    """Return all mountd partitions as a nameduple.
    If all == False return phyisical partitions only.
    """
    phydevs = []
    f = open("/proc/filesystems", "r")
    for line in f:
        if not line.startswith("nodev"):
            phydevs.append(line.strip())
    retlist = []
    bulks = get_bulks()
    f = open('/etc/mtab', "r")
    for line in f:
        if not all and line.startswith('none'):
            continue
        fields = line.split()
        device = fields[0]
        mountpoint = fields[1]
        fstype = fields[2]
        if not all and fstype not in phydevs:
            continue
        if 'mapper' in device : continue 
        if device == 'none':
            device = ''
        st = os.statvfs(mountpoint)
        uuid = None
        for bulk in bulks :
            if bulk['name'] == device : 
                uuid = bulk['uuid']

        disk = {
            'name' : device,
            'path' : mountpoint,
            'format' : fstype,
            'size' : (st.f_blocks * st.f_frsize),
            'id' : uuid
        }
        retlist.append(disk)
    return retlist

def run_cmd(cmd):
    return commands.getoutput(cmd)

def get_disk_warning():
    warning = None
    try:
        disk_cmd = "df | awk '/\<(08[5-9]|9[0-9]|100)% +/'"
        warning = os.popen(disk_cmd).read()
        if not warning:
            warning = 'normal'
    except:
        warning='Get Disk Warning Error'
    return warning

def get_mount_point_size(mount_point='/'):
    os.environ["LANGUAGE"] = "en_US:"
    cmds = "df {}".format(mount_point)
    p = subprocess.Popen(cmds, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, 
                         shell=True)
    out, err = p.communicate()
    lines  = out.split("\n")
    header_line = lines[0]
    header_columns = header_line.split()
    content_lines  = lines[1:]
    for i, column in enumerate(header_columns):
        if column == "1K-blocks":
            header_columns[i] = "Size"
    mount_point = {}
    for line in content_lines:
        columns = line.split()
        if len(line) > 3:
            for i, val in enumerate(columns):
                mount_point[header_columns[i]] = val
    return mount_point

def get_dir_size(dir_path):
    size = 0L
    for root, dirs, files in os.walk(dir_path):
        size += sum([os.path.getsize(os.path.join(root, name)) 
                     for name in files])
    return size
