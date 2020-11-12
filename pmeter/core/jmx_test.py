#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/17 10:08
# @File    : jmx_test.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
execute jmeter test.
"""

import datetime
import re

from pmeter.common.const import *
from pmeter.common.decorator import *
from pmeter.common.utils import convert_path, execute_cmd
from pmeter.core.report import get_report_list

LOGGER = logging.getLogger(__name__)
JMX_BIN = convert_path(CONF.get('Jmeter', 'JMX_BIN'))


def get_jmx_path(jmx_folder, whole_flow):
    """
    获取jmeter脚本路径
    :param jmx_folder: string--> jmeter脚本文件夹名
    :param whole_flow: bool--> 是否是完整流程
    :return: jmx_path: string--> jmeter脚本路径
    """
    if whole_flow:
        jmx_path = JMETER_FOLDER
        return jmx_path
    else:
        jmx_path = convert_path(CONF.get('Auto_Test', 'Jmx-Script'))
        if os.path.exists(jmx_path):
            return jmx_path
        else:
            jmx_path = os.path.join(os.path.join(RESULT_DIR, jmx_path), jmx_folder)
            return jmx_path


def get_rpt_path(jmx_path):
    """
    获取生成报表文件路径.
    :param jmx_path: string--> jmeter脚本路径
    :return: rpt_path: string--> 报表文件路径
    """
    rpt_path = os.path.join(os.path.dirname(jmx_path), 'report')
    return rpt_path


class BaseTest(object):
    """
    jmeter测试基类.
    """

    def __init__(self, jmx_folder='jmeter', whole_flow=False):
        self.filename_dict = dict()

        self.jmx_path = get_jmx_path(jmx_folder, whole_flow)
        self.rpt_path = get_rpt_path(self.jmx_path)

        self.result = None

        self.get_files()

        self.run()

    def get_files(self):
        """
        遍历jmeter文件夹下的所有.jmx文件
        :return: None
        """
        for root, dirs, files in os.walk(self.jmx_path):
            for filename in files:
                fullname = os.path.join(root, filename)
                if fullname.lower().endswith('.jmx'):
                    self.filename_dict[filename] = fullname

    def run(self):
        """
        遍历.jmx文件执行测试,
        支持自动浮动tps测试,
        支持指定url, threads等动态更新.
        :return: None
        """
        for filename in self.filename_dict.keys():
            threads = DEFAULT_START_THREADS
            fullname = self.filename_dict[filename]

            count = 0
            while count < LOOP_COUNT:
                count += 1

                # 更新.jmx脚本配置参数
                self.update_jmx_tps(file=fullname, threads=threads)
                log_file, cmd_str = self.log_cmd_str(filename, fullname, threads)
                current_tps = self.get_current_tps(log_file, cmd_str)

                if count == 1:
                    before_tps = current_tps
                    threads += DEFAULT_THREADS_STEP
                    continue
                else:
                    if abs((current_tps - before_tps) / before_tps) <= FLOAT_RATE:
                        break
                    else:
                        threads += DEFAULT_THREADS_STEP
                        before_tps = current_tps

            time.sleep(10)

    @KillProcess(process_name='java.exe')
    def execute_command(self, cmd_string, timeout=None):
        """
        执行测试命令函数, 支持指定超时时间.
        :param cmd_string: string--> 待执行命令字符串.
        :param timeout: float--> 超时时间.
        :return: None
        """
        if timeout:
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        sub = execute_cmd(cmd_string)
        while True:
            if sub.poll() is not None:
                break
            time.sleep(0.1)
            if timeout:
                if end_time <= datetime.datetime.now():
                    sub.kill()
                    return "TIME_OUT"

    @property
    def time_str(self):
        """
        生成时间字符串.
        :return: string
        """
        return time.strftime('%Y%m%d%H%M%S', time.localtime())

    def update_jmx_tps(self, file, threads):
        """
        替换jmeter脚本中的指定字段值
        :param file: string--> jmeter脚本文件路径
        :param threads: int--> 测试使用线程数
        :return: None
        """
        with open(file, 'r', encoding='utf-8') as f:
            data = f.read()

            # replace threads
            old_str = '<stringProp name="ThreadGroup.num_threads">[\d]{1,7}</stringProp>'
            new_str = '<stringProp name="ThreadGroup.num_threads">{threads}</stringProp>'.format(threads=threads)
            data = self.replace_str(old_str, new_str, data)

            # replace durations
            old_str = '<stringProp name="ThreadGroup.duration">[\d]{1,6}</stringProp>'
            new_str = '<stringProp name="ThreadGroup.duration">{duration}</stringProp>'.format(duration=DURATIONS)
            data = self.replace_str(old_str, new_str, data)

            # replace ip
            old_str = """((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))"""
            new_str = IP
            data = self.replace_str(old_str, new_str, data)

            # replace port
            old_str = """<stringProp name="HTTPSampler.port">[\d]{1,6}</stringProp>"""
            new_str = """<stringProp name="HTTPSampler.port">{port}</stringProp>""".format(port=PORT)
            data = self.replace_str(old_str, new_str, data)

            # replace protocol
            old_str = '<stringProp name="HTTPSampler.protocol">[a-zA-Z]{1,8}</stringProp>'
            new_str = '<stringProp name="HTTPSampler.protocol">{protocol}</stringProp>'.format(protocol=PROTOCOL)
            data = self.replace_str(old_str, new_str, data)

            # replace connect_timeout
            old_str = '<stringProp name="HTTPSampler.connect_timeout">[\d]{1,8}</stringProp>'
            new_str = '<stringProp name="HTTPSampler.connect_timeout">{connect_timeout}</stringProp>'.format(
                connect_timeout=CONNECT_TIMEOUT)
            data = self.replace_str(old_str, new_str, data)

            # replace response_timeout
            old_str = '<stringProp name="HTTPSampler.response_timeout">[\d]{1,8}</stringProp>'
            new_str = '<stringProp name="HTTPSampler.response_timeout">{response_timeout}</stringProp>'.format(
                response_timeout=RESPONSE_TIMEOUT)
            data = self.replace_str(old_str, new_str, data)

        with open(file, 'w', encoding='utf-8') as f:
            f.write(data)

    @staticmethod
    def replace_str(old_str, new_str, data):
        """
        替换字段值函数
        :param old_str: string--> 被替换的字符串
        :param new_str: string--> 替换的字符串
        :param data: string--> jmeter脚本字符串
        :return: data: string--> 更新后的jmeter脚本字符串
        """
        pattern = re.compile(old_str)
        ret = pattern.findall(data)

        if len(ret) > 0:
            old_str = ret[0]
            data = data.replace(old_str, new_str)

        return data

    def log_cmd_str(self, filename, fullname, threads) -> list:
        """
        获取日志文件路径及执行命令字符串.
        :param filename: string--> jmeter脚本文件名
        :param fullname: string--> jmeter脚本完整路径
        :param threads: int--> 测试使用线程数
        :return: [log_file, cmd_str]
        """
        pass

    @staticmethod
    def parse_jtl(file) -> float:
        """
        解析生成的.jtl文件获取上次执行的TPS
        :param file: string--> .jtl测试结果文件.
        :return: tps
        """
        pass

    def get_current_tps(self, log_file, cmd_str):
        try:
            self.execute_command(cmd_str)
        except Exception as e:
            err_msg = 'execute command error, detail:{e}'.format(e=str(e))
            LOGGER.error(err_msg)

        if os.path.exists(log_file):
            current_tps = self.parse_jtl(log_file)
            return current_tps
        else:
            err_msg = 'jtl file <{log_file}> not found!'.format(log_file=log_file)
            LOGGER.error(err_msg)
            raise FileNotFoundError(err_msg)


@log_time('Execute single interface test')
class SingleInterface(BaseTest):

    def log_cmd_str(self, filename, fullname, threads) -> list:
        log_file = os.path.join(self.rpt_path, str(threads * SLAVE_NUM) + '_' +
                                self.time_str + '_' + filename[:-4] + '.jtl')
        cmd_str = JMX_BIN + ' -n -t ' + fullname + ' -l ' + log_file
        if DISTRIBUTED_ENABLE.upper() == 'TRUE':
            cmd_str = JMX_BIN + ' -n -t ' + fullname + ' -R ' + SLAVE_IPS + ' -l ' + log_file
        print(cmd_str)
        LOGGER.info(cmd_str)
        return [log_file, cmd_str]

    @staticmethod
    def parse_jtl(file) -> tuple:
        tps, error_rate, resp_time = None, None, None
        report_list = get_report_list(jtl_file=file)
        if report_list:
            if len(report_list) > 5:
                tps, error_rate, resp_time = report_list[5], report_list[6], report_list[9]
        else:
            err_msg = 'file [{file}] var <report_list> is None'.format(file=file)
            LOGGER.error(err_msg)
            raise ValueError(err_msg)
        if tps:
            return tps
        else:
            err_msg = 'file [{file}] tps is None'.format(file=file)
            LOGGER.error(err_msg)
            raise ValueError(err_msg)
