# -*- coding: utf-8 -*-

import vobject
import warnings
from urllib.parse import urlparse
import logging
from datetime import datetime, timezone
from platform import system, release
from tzlocal import get_localzone
import sys
from requests import request

PROD_ID = '//taskwarrior/{system} {release}/EN'
logger = logging.getLogger(__name__)
logger.propagate = True

if logger.level >= 10:
    try: # for Python 3
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection
    HTTPConnection.debuglevel = 1

# TODO: Figure out how to deal with warning messages
warnings.filterwarnings(
    "ignore",
    message="The zone attribute is specific to pytz's interface",
    append=True
)
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
    append=True
)

# TODO:
# Maybe use a tag or something to disable importing task to ical
# Use jinja to add task properties as tags using `add_tags_template` config prop

def is_uri(uri):
    """
        True, if uri is valid uri. Must contain http schema and address to be valid
        eg. https://example.com/ or https://example.com/path

    """
    try:
        parsed_uri = urlparse(uri)
        return all([parsed_uri.scheme, parsed_uri.netloc])
    except:
        return False

def get_system(platform):
    '''
    Return the system based off the running platform (eg. linux)
    '''
    if 'linux' in platform:
        system = 'Linux'
    elif 'bsd' in platform:
        system = 'BSD'
    elif 'darwin' in platform:
        system = 'MacOS'
    else:
        system = 'Windows'
    return system

def merge_task(original, modified):
    """ Merge original task with modified task  """
    task = {}
    if not modified:
        return original
    for prop in modified:
        if (prop in original and original[prop] != modified[prop])\
                or not prop in original:
            task[prop] = modified[prop]
        elif not prop in modified:
            task[prop] = None
        else:
            task[prop] = original[prop]
    return task

def urljoin(*args):
    return '/'.join(map(lambda x: str(x).rstrip('/'), args))

def generate_cal_url(task, cal, config):
    """ Generate calendar url for new task """
    cal_base_url = config.get(section='general', option='default_calendar')

    generated_ics_file_path = '{uid}.ics'.format(uid=cal.vtodo.uid.value)
    if 'project' in task:
        displayname = task['project']
        if not config.has_section(displayname):
            if config.get(section='general', option='default_calendar'):
                return urljoin(
                    config.get(section='general', option='default_calendar'),
                    generated_ics_file_path
                )
            else:
                logger.warn('Could not find a calendar to import task {} to'.format(task['uuid']))
                sys.exit(0)
        cal_base_url = config.get(section=displayname, option='url')
    return urljoin(cal_base_url, generated_ics_file_path)

def send_ical_to_server(ical, url, config):
    """ Send icalendar event to calendar server"""
    try:
        headers = {
            "Content-Type": "text/calendar",
        }
        method = 'delete'
        data = None
        if ical.vtodo.status.value != 'CANCELLED':
            method = 'put'
            data = ical.serialize()
            headers['Content-Length'] = str(len(ical.serialize()))
        request(
            method=method,
            url=url,
            data=data,
            auth=config.auth,
            headers=headers
        )
    except Exception as e:
        logger.error('ERROR: {0}'.format(e))
        print('ERROR: ', e)
        sys.exit(1)

def get_rfc_datetime(value):
    """ Taskwarrior datetime string --> datetime RFC spec."""
    if isinstance(value, str):
        dt = datetime.strptime(value, '%Y%m%dT%H%M%SZ')
    else:
        dt = value

    return dt.replace(tzinfo=timezone.utc).astimezone(get_localzone())

def task_to_ical(original, modified):
    """ Taskwarrior --> iCalendar vobject."""

    task = merge_task(original, modified)
    ical = vobject.iCalendar()
    ical.add('prodid').value = PROD_ID.format(release=release(), system=system())
    ical.add('vtodo')
    vobj = ical.vtodo

    if 'uid' not in vobj.contents:
        if 'uid' in original:
            vobj.add('uid').value = original['uid']
        else:
            vobj.add('uid').value = original['uuid']
            original['uid'] = vobj.uid.value
        vobj.add('created').value = get_rfc_datetime(datetime.utcnow())
    if 'description' in task:
        vobj.add('summary').value = task['description']
    if 'annotations' in task:
        annotations = '\n'.join(str(annotation['description']) for annotation in task['annotations'])
        vobj.add('description').value = annotations
    if 'entry' in task:
        vobj.add('dtstamp').value = get_rfc_datetime(task['entry'])
    if 'start' in task or 'wait' in task:
        dstart = task['wait'] if 'wait' in task else task['start']
        vobj.add('dtstart').value = get_rfc_datetime(dstart)
    if 'end' in task:
        vobj.add('completed').value = get_rfc_datetime(task['end'])
    if 'modified' in task:
        vobj.add('last-modified').value = get_rfc_datetime(task['modified'])
    if 'priority' in task:
        priority = {
            'H': '0',
            'M': '5',
            'L': '10'
        }
        vobj.add('priority').value = priority.get(str(task['priority']), None)
    if 'due' in task:
        vobj.add('due').value = get_rfc_datetime(task['due'])
    if 'recu' in task or 'until' in task:
        rrule = vobj.add('rrule')
        rrule['freq'] = task['recu'] if 'recu' in task else None
        rrule['until'] = task['until'] if 'until' in task else None
    if 'status' in task:
        vtodo_status = {
            'pending':   'NEEDS-ACTION',
            'completed': 'COMPLETED',
            'deleted':   'CANCELLED',
            'waiting':   'IN-PROCESS'
        }
        ical_status = {
            'waiting': 'TENATIVE',
            'deleted': 'CANCELLED'
        }
        vobj.add('status').value = vtodo_status.get(task['status'], None)
        ical.add('status').value = ical_status.get(task['status'], 'CONFIRMED')
    if 'tags' in task:
        vobj.add('categories').value = task['tags']
    if 'geo' in task:
        vobj.add('geo').value = task['geo']

    return ical
