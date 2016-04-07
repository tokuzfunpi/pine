"""!Network Func
@package pine.network
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 15:00:00
"""
import netaddr
from pine.cmd import execute
from urlparse import urlparse
import socket

def check_ip_format(ip):
    result = netaddr.valid_ipv4(ip, flags=1)
    return result

def check_netmask_format(netmask):
    try:
        result = netaddr.IPAddress(netmask).is_netmask()
        return result
    except netaddr.core.AddrFormatError:
        return False

def convert_to_cidr(ip, netmask):
    netmask_bit = netaddr.IPAddress(netmask).bits()
    network_prefix = str(netmask_bit.count("1"))
    temp_cidr = "/".join([ip, network_prefix])
    result = str(netaddr.IPNetwork(temp_cidr).cidr)
    return result

def is_ip_in_network(ip, cidr):
    return netaddr.IPAddress(ip) in netaddr.IPNetwork(cidr)

def ping(ip, time=1):
    cmd = 'ping -c {0} {1}'.format(time, ip)
    status, err = execute(cmd, status=True)
    if status != 0:
        return False
    return True

def check_addr(addr):
    _url = urlparse(addr)
    hostname = get_real_ip(_url.hostname)
    port = str(_url.port)
    return _url.scheme + '://' + hostname + ':' + port

def get_real_ip(addr):
    try :
        _addr = socket.gethostbyname(addr)
    except Exception :
        _addr = '127.0.0.1'
    return _addr

def get_ip_from_host(hostname):
    cmd_str = "cat /etc/hosts | grep %s | cut -f 1" % hostname
    return execute(cmd_str)

def get_ext_iface_name():
    possible_target = "br-srv"
    cmd_str = "ifconfig -a | grep %s" % possible_target
    res = execute(cmd_str)
    if not res :
        return "br-mg"
    else :
        return "br-srv"

def get_iface_netmask(iface):
    cmd_str = "ifconfig %s | grep Mask | cut -d':' -f4" % iface
    return execute(cmd_str)

def bind_ip_alias(ip_addr, iface, net_mask, alias_name="upgrade"):
    cmd = "ifconfig {0}:{1} {2} netmask {3}".format(iface, alias_name, ip_addr,
                                                    net_mask)
    status, err = execute(cmd, status=True)
    if status != 0:
        raise Exception("ip alias binding failed")

    # send arping -A -I br-mg <ip>
    cmd = 'arping -c 10 -A -I {0} {1}'.format(iface, ip_addr)
    status, err = execute(cmd, status=True)
    if status != 0:
        raise Exception("arping failed")
