# -*- coding: utf-8 -*-

import vobject
import uuid
import urllib.parse as urlparse
from datetime import datetime, timezone
from platform import system, release
from tzlocal import get_localzone
import json
import sys
import os
from requests import auth, put, request


# TODO:
# Handle logs
# Move code into other modules
# Maybe use a tag or something to disable importing task to ical

def urljoin(*args):
    return '/'.join(map(lambda x: str(x).rstrip('/'), args))

def generate_cal_url(task, cal, config):
    """ Generate calendar url for new task """
    cal_base_url = config.get(section='general', option='base_url')
    generated_ics_file_path = '{uid}.ics'.format(uid=cal.vtodo.uid.value)
    if config.getboolean(section='general', option='use_project_as_displaynames') and 'project' in task:
        displayname = task['project']
        if not config.has_section(displayname):
            sys.exit(0)
        cal_base_url = config.get(section=displayname, option='url')
    return urljoin(cal_base_url, generated_ics_file_path)

def send_ical_to_server(ical, url, config):
    """ Send icalendar event to calendar server"""
    try:
        headers = {
            "Content-Type": "text/calendar",
            "Content-Length": str(len(ical.serialize()))
        }
        method = 'delete' if ical.vtodo.status == 'CANCELLED' else 'put'
        data = None if method == 'delete' else ical.serialize()
        request(
            method=method,
            url=url,
            data=data,
            auth=config.auth,
            headers=headers
        )
    except Exception as e:
        print('ERROR: ', e)
        sys.exit(1)

def get_rfc_datetime(value):
    """ Taskwarrior datetime string --> datetime RFC spec."""
    if isinstance(value, str):
        dt = datetime.strptime(value, '%Y%m%dT%H%M%SZ')
    else:
        dt = value
    return dt.replace(tzinfo=timezone.utc).astimezone(get_localzone())

def task_to_ical(task, config):
    """ Taskwarrior --> iCalendar vobject."""

    if 'status' in task and task['status'] != 'pending' and not 'uid' in task:
        return

    ical = vobject.iCalendar()
    ical.add('prodid').value = config.get(section='general', option='prod_id_template').format(release=release(), system=system())
    ical.add('vtodo')
    vobj = ical.vtodo

    if not 'uid' in task:
        vobj.add('uid').value = task['uuid']
        task['uid'] = vobj.uid.value
        vobj.add('created').value = get_rfc_datetime(datetime.utcnow())
    if 'description' in task:
        vobj.add('summary').value = task['description']
    if 'annotations' in task:
        vobj.add('summary').value = '\n'.join(task['description'] + task['annotations'])
    if 'entry' in task:
        vobj.add('dtstamp').value = get_rfc_datetime(task['entry'])
    if 'start' in task:
        vobj.add('dtstart').value = get_rfc_datetime(task['start'])
    if 'end' in task:
        vobj.add('dtend').value = get_rfc_datetime(task['end'])
    if 'modified' in task:
        vobj.add('last-modified').value = get_rfc_datetime(task['modified'])
    if 'priority' in task:
        priority = {
            'H': 0,
            'M': 5,
            'L': 10
        }
        vobj.add('priority').value = priority.get(task['priority'], None)
    if 'due' in task:
        vobj.add('due').value = get_rfc_datetime(task['due'])
    if 'recu' in task or 'until' in task:
        rrule = vobj.add('rrule')
        rrule['freq'] = task['recu'] if 'recu' in task else None
        rrule['until'] = task['until'] if 'until' in task else None
    if 'status' in task:
        status = {
            'pending': 'NEEDS-ACTION',
            'completed': 'COMPLETED',
            'deleted': 'CANCELLED'
        }
        vobj.add('status').value = status.get(task['status'], None)
    if 'tags' in task:
        vobj.add('categories').value = task['tags']
    if 'geo' in task:
        vobj.add('geo').value = task['geo']

    print(json.dumps(task))
    return ical

