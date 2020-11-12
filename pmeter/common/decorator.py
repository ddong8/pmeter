#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/17 10:05
# @File    : decorator.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
decorators used for log,send message, kill process etc.
"""

import logging
import sys
from functools import wraps

from pmeter.common.const import datetime_str
from pmeter.common.utils import execute_cmd

LOGGER = logging.getLogger(__name__)


def log_time(action_name=''):
    """
    record func execute time.
    :param action_name: str --> function name
    :return: None
    """

    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if not action_name:
                action = func.__name__
            else:
                action = action_name
            start_msg = "start <{action}> at {datetime_str}..." \
                .format(action=action, datetime_str=datetime_str())
            LOGGER.info(start_msg)
            print(start_msg)
            func(*args, **kwargs)
            end_msg = "end <{action}> at {datetime_str}..." \
                .format(action=action, datetime_str=datetime_str())
            LOGGER.info(end_msg)
            print(end_msg)

        return wrapped_function

    return logging_decorator


class ExecuteOnlyOnLinux(object):
    """
    execute function on Linux platform.
    """

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if sys.platform == 'linux':
                func(*args, **kwargs)

        return wrapped_function


class KillProcess(object):
    """
    kill jmeter process base on os platform.
    """

    def __init__(self, process_name='java.exe'):
        self.process_name = process_name

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            self.kill_process()
            func(*args, **kwargs)
            self.kill_process()

        return wrapped_function

    def kill_process(self):
        if sys.platform == 'win32':
            self.process_name = 'java.exe'
            cmd_string = 'TASKKILL /F /IM {process_name} /T' \
                .format(process_name=self.process_name)
            execute_cmd(cmd_string)
        elif sys.platform == 'linux':
            self.process_name = 'java'
            cmd_string = 'pkill -f {process_name}' \
                .format(process_name=self.process_name)
            execute_cmd(cmd_string)
