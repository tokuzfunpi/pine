"""!Cmd Functions
@package pine.libvirt
@author Joe.Yang <tokuzfunpi@gmail.com>
@date 2015-10-27 15:40:00
"""
import libvirt

def _connect_to_libvirt():
    conn = libvirt.open()
    if conn == None:
        raise Exception('Failed to open connection to the hypervisor')
    return conn

def list_domains():
    conn = _connect_to_libvirt()
    try:
        domains = conn.listAllDomains()
    except:
        raise Exception('Failed to get domains')
    return domains

def destroy_domains(domains):
    for dom in domains:
        try:
            dom.destroy()
        except:
            raise Exception('Failed to destroy domains')

def undefine_domains(domains):
    for dom in domains:
        try:
            dom.undefine()
        except:
            raise Exception('Failed to undefine domains')
