"""!JSON utils
@package pine.json
@author Joe Yang <tokuzfunpi@gmail.com>
@date 2015-7-7 10:50:00
"""
import json

def json_dump(_obj, _ascii=False, **kwargs):
    '''!dump dict to json object
    @param _obj dict to json
    @retval Object json object
    '''
    return json.dumps(_obj, ensure_ascii=_ascii, **kwargs)

def json_load(_obj):
    '''!dump dict to json object
    @param _obj dict to json
    @retval Object json object
    '''
    try:
        result = json.loads(_obj)
    except:
        raise ValueError('Wrong JSON')
    return result
