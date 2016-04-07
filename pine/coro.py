#!/usr/bin/env python
from commands import getstatusoutput as _run
import os
from pine.service import service_start, service_stop
from pine.utils import sleep, get_node

GET_DC_HN_CMD = '''crm_mon -r1 | grep 'Current DC:' | cut -d' ' -f 3'''
GET_DC_OBJ_ID_CMD = '''crm_mon -r1 | grep 'Current DC:' | cut -d' ' -f 4'''
GET_OBJ_IP_CMD = '''corosync-cmapctl | grep {obj_id} | grep ip'''

def get_dc_info():
    # Start coro sync
    service_start('corosync')
    service_start('pacemaker')
    sleep(5)
    result = {
        'dc_host' : None,
        'dc_ip' : None
    }
    ret, res = _run(GET_DC_OBJ_ID_CMD)
    if ret > 0 :
        # COROSYNC OR Pacemaker not ready
        service_stop('corosync')
        service_stop('pacemaker')
        raise Exception('Corosync not ready')
    if res == '':
        # No dc case
        return {
            'dc_host' : get_node(),
            'dc_ip' : "127.0.0.1"
        }
    obj_id = res.strip('(').strip(')')
    ret, res = _run(GET_OBJ_IP_CMD.format(obj_id=obj_id))
    if ret > 0:
        # COROSYNC OR Pacemaker not ready
        service_stop('corosync')
        service_stop('pacemaker')
        raise Exception('Corosync not ready')
    dc_ip = res.split('ip(')[-1].replace(')','').strip()

    ret, dc_hn_name = _run(GET_DC_HN_CMD)
    if ret > 0 :
        # COROSYNC OR Pacemaker not ready
        service_stop('corosync')
        service_stop('pacemaker')
        raise Exception('Corosync not ready')
    # Stop coro sync
    service_stop('corosync')
    service_stop('pacemaker')
    return {
        'dc_host' : dc_hn_name,
        'dc_ip' : dc_ip
    }
