#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Adds taskwarrior tasks into a calendar as iCal tasks

# Install the required python packages
# $ pip install requests
# $ pip install vobject


from icaltask.config import load_config
from icaltask.utils import task_to_ical, generate_cal_url, send_ical_to_server
import sys
import json

# TODO:
# Handle logs
# Move code into other modules
# Maybe use a tag or something to disable importing task to ical

old = sys.stdin.readline()
new = sys.stdin.readline()
config = load_config()

try:
    if not new:
        task = json.loads(old)
    else:
        task = json.loads(new)
    cal = task_to_ical(task, config)

    url = generate_cal_url(task, cal, config)

    if cal:
        send_ical_to_server(cal, url, config)
except IOError as e:
    print('WARN: %s', e)
    sys.exit(0)
