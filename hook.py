#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-

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
TASK_TYPE = 'new'

try:
    if not new:
        original_task = json.loads(old)
        modified_task =  None
        task = json.loads(old)
    else:
        original_task = json.loads(old)
        modified_task = json.loads(new)
        task = json.loads(new)
        TASK_TYPE = 'modified'

    logger.debug('Original JSON %s', old.strip('\n'))
    if TASK_TYPE == 'modified':
        logger.debug('Modified JSON %s', new.strip('\n'))
    cal = task_to_ical(original_task, modified_task)

    url = generate_cal_url(task, cal, config)
    logger.info('url %s', url)
    logger.debug('Importing %s task %s to calendar %s', TASK_TYPE, task['uuid'], url)

    if cal:
        logger.debug('CAL %s', cal.serialize())
        send_ical_to_server(cal, url, config)
except IOError as error:
    logger.warn('WARN: %s', error)
    sys.exit(0)
