#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/18 10:21
# @File    : utils.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
some util functions.
"""

import logging
import os
import socket
import subprocess

import xlrd

from pmeter.common import const

LOGGER = logging.getLogger(__name__)


def get_host_ip():
    """
    get local ip.
    :return:
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def start_threads_dict():
    """
    获取指定URL起始THREADS字典
    :return: dict-->配置中指定URL起始THREADS字典
    """
    temp_dict = dict()
    enable_flag = const.CONF.get('Auto_Test.assign_start_threads', 'ENABLE')
    if enable_flag and isinstance(enable_flag, str):
        if enable_flag.lower() == 'true':
            temp_dict = const.CONF['Auto_Test.assign_start_threads']
    return temp_dict


def convert_path(path: str) -> str:
    """
    将路径按当前系统路径分割符转换
    :param path: str -->原始路径字符串
    :return: str -->转换后的字符串
    """
    return path.replace(r'\/'.replace(os.sep, ''), os.sep)


def check_dir(path):
    """
    检查指定路径是否存在,不存在创建
    :return: None
    """
    # 检查jmeter脚本csv配置文件夹是否存在
    if not os.path.exists(path):
        os.makedirs(path)


def read_config(config_path):
    """
    读取配置文件并返回配置字典
    :param config_path: str-->配置文件路径
    :return: url_dict: dict-->配置字典
    """
    wb = xlrd.open_workbook(config_path)
    table = wb.sheets()[0]
    nrows = table.nrows

    url_dict = dict()

    for i in range(1, nrows):
        if table.cell_value(i, 0):
            url = table.cell_value(i, 0)
            url_dict[url] = url

    return url_dict


def read_rate_csv(url_rate_file):
    """
    读取url占比字典.
    :param: url_rate_file: string--> url占比文件名
    :return: url_rate_dict: dict--> url占比字典
    """
    url_rate_dict = dict()
    with open(url_rate_file) as f:
        for line in f:
            temp_arr = line.split(",")
            url_rate_dict[temp_arr[0]] = temp_arr[2]
    url_rate_dict.pop('url')
    return url_rate_dict


def execute_cmd(cmd_string):
    """
    使用 subprocess 执行系统命令.
    :param cmd_string: string--> 待执行命令字符串.
    :return: None
    """
    sub = subprocess.Popen(cmd_string,
                           universal_newlines=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           bufsize=4096,
                           shell=True)
    out, err = sub.communicate()
    if out:
        print(out)
        LOGGER.info(out)
    if err:
        print(err)
        LOGGER.error(err)
    return sub
