#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/12 16:24
# @File    : action.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
detail command func.
"""

import logging

from pmeter.common import const
from pmeter.common.logger import initialize_logger
from pmeter.common.utils import check_dir
from pmeter.core.jmx_test import SingleInterface
from pmeter.core.report import GenerateReport
from pmeter.core.upload import restart_slave, upload_file

LOGGER = logging.getLogger(__name__)


def execute_restart():
    """
    restart slave jmeter-server.
    :return: None
    """
    restart_slave()


def execute_distribute():
    """
    execute distribute csv config file to slave.
    :return: None
    """
    upload_file()


def execute_auto_exe():
    """
    execute auto single jmeter script.
    :return: None
    """
    SingleInterface()


def execute_report():
    """
    execute auto generate report from .jtl file
    :return: None
    """
    GenerateReport()


def execute_actions(sub_command, cmd_list):
    """
    execute command from input params.
    :param sub_command: str --> command name
    :param cmd_list: list --> command list
    :return: None
    """
    func_list = [execute_restart, execute_distribute, execute_auto_exe, execute_report]

    if len(cmd_list) == len(func_list):
        for i in range(len(cmd_list)):
            if sub_command == cmd_list[i]:
                exec_func = func_list[i]
                initialize_app()
                exec_func()
                break


def initialize_app():
    """
    initialize application.
    :return: None
    """
    # initialize dir
    for dir_name in [const.LOG_DIR, const.RESULT_DIR]:
        check_dir(dir_name)

    # initialize log
    initialize_logger()
