"""!Utils
@package pine.utils
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 10:50:00
"""
import time
import uuid
import string
import random
import socket
import md5
import hashlib
from datetime import datetime
from subprocess import check_output

def get_pid(name):
    return check_output(["pidof", name]).rstrip()

def get_file_checksum(file_path):
    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()

def md5_hash(_str):
    return md5.new(_str).hexdigest()

def sleep(sec=0.1):
    time.sleep(sec)

def get_node():
    return socket.gethostname()

def current_timestamp(scope=1000):
    '''!get current timestamp(ms)
    @retval Int current timestamp
    '''
    return int(round(time.time()*scope))

def ts_func():
    '''!get current timestamp(ms)
    @retval Int current timestamp
    '''
    return lambda: int(round(time.time()*1000))

def get_uuid(_hex=False):
    '''!get uuid
    @retval String uuid
    '''
    if _hex :
        return str(uuid.uuid4().hex)
    else :
        return str(uuid.uuid4())

def check_utf8(string):
    """
    Validate if a string is valid UTF-8 str or unicode and that it
    does not contain any null character.

    :param string: string to be validated
    :returns: True if the string is valid utf-8 str or unicode and
              contains no null characters, False otherwise
    """
    if not string:
        return False
    try:
        if isinstance(string, unicode):
            string.encode('utf-8')
        else:
            string.decode('UTF-8')
        return '\x00' not in string
    # If string is unicode, decode() will raise UnicodeEncodeError
    # So, we should catch both UnicodeDecodeError & UnicodeEncodeError
    except UnicodeError:
        return False

def name_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def convert_datetime_to_timestamp(datetime_object, tz=False):
    '''!conver datetime_object to timestamp
    @param datetime_object datetime object
    @param tz timezone
    @retval time stamp
    '''
    result=time.mktime(datetime_object.timetuple())
    if tz:
        result -= time.timezone
    return result

def convert_ts_to_datetime(timestamp):
    '''!conver datetime_object to timestamp
    @param datetime_object datetime object
    @param tz timezone
    @retval time stamp
    '''
    return datetime.fromtimestamp(float(timestamp))
