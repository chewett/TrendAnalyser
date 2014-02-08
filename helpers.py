import json
import errno
from dateutil import parser
import calendar

def convert_to_unix(timestamp):
    '''Used to convert any timestamp format to unix time'''
    return calendar.timegm(parser.parse(timestamp).utctimetuple())

def save_data(json_data, location):
    '''Saves json data to a specific file location'''
    try:
        os.makedirs(os.path.dirname(location))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    json.dump(json_data, open(location, 'w'))

