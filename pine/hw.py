"""!Hardware Functions
@package pine.hw
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 10:50:00
"""
import socket
import os
import platform
import psutil
import multiprocessing
from pine.cmd import run_simple_cmd

def check_numa_enable():
    _cmd = "numactl --hardware  | grep 'available:' | awk '{print $2}'"
    res = int(run_simple_cmd(_cmd))
    if res <= 1 :
        return False
    else :
        return True

def get_cpu_usage():
    return psutil.cpu_percent(interval=1.0)

def get_cpu_cores():
    cores = multiprocessing.cpu_count()    
    return cores

def cpu_data():
    res = os.popen("lscpu")
    data = dict()
    tmp_data = dict()
    for line in res.readlines() :
        _line = line.split(":")
        tmp_data[_line[0]] = _line[1].strip().split("\n")[0]
    data["numa_node"] = int(tmp_data["NUMA node(s)"])
    data["socket"] = int(tmp_data["Socket(s)"])
    data["core_per_socket"] = int(tmp_data["Core(s) per socket"])
    data["thread_per_core"] = int(tmp_data["Thread(s) per core"])
    data["architecture"] = tmp_data["Architecture"]
    data['info'] = cpu_info()
    data['total_core'] = get_cpu_cores()
    #Generate numa topology
    numa_topos = []
    numa_key_template = "NUMA node%d CPU(s)"
    for _n in range(data["numa_node"]) :
        _target_key = numa_key_template % _n
        topology = {
            "node" : _n,
            "cpu" : tmp_data[_target_key]
        }
        numa_topos.append(topology)
    data["numa_topology"] = numa_topos
    return data

def cpu_info():
    cpu_info = None       
    infos = "cat /proc/cpuinfo | grep 'model name' | awk -F: '{print $2}'"
    info = os.popen(infos).read()
    cpu_info = info.strip().split("\n")[0]
    return cpu_info

def get_inner_ip_mac():  
    inner_ip = None
    inner_mac = None    
    ip_line = "ifconfig | grep 'inet addr' | awk -F: '{print $2}' | awk \
             '{print $1}' | grep -v 127.0.0.1 "
    ips = os.popen(ip_line).read()
    ip = ips.split('\n')
    mac_line = "ifconfig | grep HWaddr | awk -F' ' '{print $5}'"
    macs = os.popen(mac_line).read()
    mac = macs.split('\n')
    j = 0
    for _ip in ip:
        if _ip:
            if _ip.startswith('172.18') or _ip.startswith('172.20') or \
               _ip.startswith('192.168')or _ip.startswith('10.') or \
               _ip.startswith('0.0.') or _ip.startswith('127.0.'):
                inner_ip = _ip
                inner_mac = mac[j]
                break
            else:
                j = j + 1
    return inner_ip, inner_mac

def get_os():
    return platform.platform()

def get_system():
    return platform.system()

def hostname():
    try:
        hostname = socket.gethostname()
        return str(hostname)
    except:
        return 'Unkown_hostname'

def sys_dir():
    path = None
    path = os.getcwd()
    return str(path)
      
def get_phy_mem():
    return int(psutil.TOTAL_PHYMEM) / 1024

def get_avail_mem():
    return int(psutil.avail_phymem()) / 1024

def get_used_mem():
    return int(psutil.used_phymem()) / 1024
