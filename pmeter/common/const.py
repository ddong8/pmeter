#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 8:57
# @File    : const.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
constant for application.
"""

import os
import time

from pmeter.common.config import CONF, base_dir


def time_str():
    """
    time string format like '20200331091759'.
    :return: string
    """
    return time.strftime('%Y%m%d%H%M%S', time.localtime())


def datetime_str():
    """
    datetime string format like '2020-03-31 09:18:10'.
    :return: string
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


# target server
PROTOCOL = CONF.get('Target-Server', 'PROTOCOL')
IP = CONF.get('Target-Server', 'IP')
PORT = CONF.get('Target-Server', 'PORT')
CONNECT_TIMEOUT = CONF.get('Target-Server', 'CONNECT_TIMEOUT')
RESPONSE_TIMEOUT = CONF.get('Target-Server', 'RESPONSE_TIMEOUT')

# auto test
DISTRIBUTED_ENABLE = CONF.get('Auto_Test', 'DISTRIBUTED_ENABLE')
SLAVE_IPS = CONF.get('Auto_Test', 'SLAVE_IPS')

SLAVE_NUM = 1
if DISTRIBUTED_ENABLE.lower() == 'true':
    SLAVE_NUM = len(SLAVE_IPS.split(','))

DURATIONS = CONF.get('Auto_Test', 'DURATIONS')
DEFAULT_START_THREADS = int(int(CONF.get('Auto_Test', 'DEFAULT_START_THREADS')) / SLAVE_NUM)
DEFAULT_THREADS_STEP = int(int(CONF.get('Auto_Test', 'DEFAULT_THREADS_STEP')) / SLAVE_NUM)
FLOAT_RATE = float(CONF.get('Auto_Test', 'FLOAT_RATE')) * 0.01
LOOP_COUNT = int(CONF.get('Auto_Test', 'LOOP_COUNT'))

# project base dir
BASE_DIR = base_dir

# project most useful folder
CONF_DIR = os.path.join(BASE_DIR, 'etc')
RESULT_DIR = os.path.join(BASE_DIR, 'result')
LOG_DIR = os.path.join(BASE_DIR, 'log')

# base on current time, generate new folder under RESULT_DIR
DATETIME_FOLDER = os.path.join(RESULT_DIR, time_str())

JMETER_FOLDER = os.path.join(DATETIME_FOLDER, 'jmeter')
REPORT_FOLDER = os.path.join(DATETIME_FOLDER, 'report')
CSV_FOLDER = os.path.join(JMETER_FOLDER, 'csv')
