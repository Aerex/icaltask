#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-

# Adds taskwarrior tasks into a calendar as iCal tasks

# Install the required python packages
# $ pip install requests
# $ pip install vobject


from icaltask.config import load_config
from icaltask.utils import task_to_ical, generate_cal_url, send_ical_to_server
import sys
import json
import logging

logger = logging.getLogger(__name__)

# TODO:
# Maybe use a tag or something to disable importing task to ical

old = sys.stdin.readline()
new = sys.stdin.readline()
config = load_config()
task_type = 'modified'

try:
    if not new:
        task = json.loads(old)
    else:
        task = json.loads(new)
        task_type = 'new'

    cal = task_to_ical(task, config)

    url = generate_cal_url(task, cal, config)
    logger.debug('Importing {task_type} task {id} to calendar {url}'.format(task_type=task_type, id=task['uuid'], url=url))
    logger.debug(json.dumps(task))

    if cal:
        send_ical_to_server(cal, url, config)
except IOError as e:
    logger.warn('WARN: %s', e)
    sys.exit(0)
