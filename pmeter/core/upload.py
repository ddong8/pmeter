#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 15:07
# @File    : upload.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
upload csv config file to slave host.
"""

import os

from pmeter.common import const
from pmeter.common.decorator import ExecuteOnlyOnLinux
from pmeter.common.utils import convert_path
from pmeter.core.jmx_test import JMX_BIN


def init_cmd():
    ips = const.SLAVE_IPS.split(',')
    if os.path.exists(const.JMETER_FOLDER):
        jmx_path = const.JMETER_FOLDER
    else:
        jmx_path = convert_path(const.CONF.get('Auto_Test', 'Jmx-Script'))
        if not os.path.exists(jmx_path):
            jmx_path = os.path.join(os.path.join(const.RESULT_DIR, jmx_path), 'jmeter')
    csv_folder = os.path.join(jmx_path, 'csv')
    csv_path = csv_folder + os.sep
    jmx_bin_dir = os.path.dirname(JMX_BIN)
    target_path = os.sep.join(csv_path.split(os.sep)[:-2])
    jmeter_server = '{jmx_server} > /dev/null 2>&1 &'.format(jmx_server=os.path.join(jmx_bin_dir, 'jmeter-server'))
    kill_cmd = 'pkill -f jmeter'
    remove_log_cmd = 'rm -f {log_name}'.format(log_name=os.path.join(jmx_bin_dir, 'jmeter-server.log'))
    return [ips, csv_path, target_path, jmx_bin_dir, jmeter_server, kill_cmd, remove_log_cmd]


@ExecuteOnlyOnLinux()
def restart_slave():
    """
    重启slave机上的jmeter-server
    :return:
    """
    cmd = init_cmd()
    ips, jmx_bin_dir, jmeter_server, kill_cmd, remove_log_cmd = cmd[0], cmd[3], cmd[4], cmd[5], cmd[6]
    for ip in ips:
        print('restart slave jmeter server at {ip} ...'.format(ip=ip))
        os.system('ssh {ip} {kill_cmd}'.format(ip=ip, kill_cmd=kill_cmd))
        os.system('ssh {ip} {remove_log_cmd}'.format(ip=ip, remove_log_cmd=remove_log_cmd))
        os.system('ssh {ip} "cd {jmx_bin_dir};{jmeter_server}"'.format(ip=ip,
                                                                       jmx_bin_dir=jmx_bin_dir,
                                                                       jmeter_server=jmeter_server))


@ExecuteOnlyOnLinux()
def upload_file():
    """
    推送csv配置文件到各个slave机
    :return:
    """
    cmd = init_cmd()
    ips, csv_path, target_path = cmd[0], cmd[1], cmd[2]
    for ip in ips:
        print('send file to {ip} ...'.format(ip=ip))
        os.system('ssh {ip} mkdir -p {target_path}'.format(ip=ip, target_path=target_path))
        os.system('scp -r {csv_path} {ip}:{target_path}'.format(csv_path=csv_path, ip=ip, target_path=target_path))
