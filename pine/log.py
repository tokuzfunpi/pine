"""!Logger
@package pine.log
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 10:30:00
"""
from swift.common.utils import get_logger as swift_get_logger

def get_logger(conf, name=None, log_to_console=False, log_route=None,
               fmt="%(levelname)s %(server)s: %(message)s"):
    return swift_get_logger(conf, 
                            name=conf.get('log_name', name),
                            log_to_console=log_to_console,
                            log_route=log_route,
                            fmt=fmt)

