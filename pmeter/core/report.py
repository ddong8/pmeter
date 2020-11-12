#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 14:25
# @File    : report.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
generate report from .jtl file.
"""

import csv
import logging
import os
import re
import time

import pandas as pd

from pmeter.common import const
from pmeter.common.decorator import log_time
from pmeter.common.utils import convert_path

LOGGER = logging.getLogger(__name__)


def get_jtl_path(whole_flow):
    """
    获取.jtl文件路径
    :param whole_flow: bool--> 是否完整流程
    :return: jtl_path: string--> .jtl文件路径
    """
    if whole_flow:
        jtl_path = const.REPORT_FOLDER
        return jtl_path
    else:
        jtl_path = convert_path(const.CONF.get('Gen_Report', 'JTL'))
        if os.path.exists(jtl_path):
            return jtl_path
        else:
            jtl_path = os.path.join(os.path.join(const.RESULT_DIR, jtl_path), 'report')
            return jtl_path


def get_rpt_path(jtl_path):
    """
    获取生成的报表文件路径
    :param jtl_path: string--> .jtl文件路径
    :return: rpt_path: string--> 报表文件路径
    """
    rpt_path = os.path.join(jtl_path, const.CONF.get('Gen_Report', 'REPORT'))
    return rpt_path


@log_time('Generate report')
class GenerateReport(object):
    """
    根据测试结果.jtl生成报表
    """

    def __init__(self, whole_flow=False):
        self.df = None
        self.jtl_file_path = get_jtl_path(whole_flow)
        self.rpt_file_path = get_rpt_path(self.jtl_file_path)

        self.header_list = ['Label', 'Start Time', 'End Time', 'Durations s', 'Threads', 'TPS /sec',
                            'Error rate', 'Min req_time ms', 'Max req_time ms', 'Avg req_time ms', 'Samples',
                            'Sent KB/sec', 'Received KB/sec', 'Avg latency ms', 'Min latency ms', 'Max latency ms']

        self.generate_df()
        self.export_csv()

    def export_csv(self):
        """
        输出报表csv文件
        :return: None
        """
        index = self.df.sort_values(by=['Label', 'Threads', 'TPS /sec']).index
        ndf = self.df.reindex(index)
        ndf.to_csv(self.rpt_file_path, index=False)

    def generate_df(self):
        """
        生成pandas dataFrame
        :return: df: dataFrame-->提取结果dataFrame
        """
        report_dict = dict()

        for col in self.header_list:
            report_dict[col] = []

        for root, dirs, files in os.walk(self.jtl_file_path):
            for filename in files:
                fullname = os.path.join(root, filename)
                if fullname.lower().endswith('.jtl'):
                    report_list = get_report_list(fullname)
                    if report_list:
                        for i in range(0, len(self.header_list)):
                            report_dict[self.header_list[i]].append(report_list[i])

        self.df = pd.DataFrame.from_dict(report_dict)


def get_report_list(jtl_file):
    """
    parse .jtl file,get the test result.
    :param jtl_file: string --> .jtl file path.
    :return: list --> return test result list.
    """
    df = None
    try:
        df = pd.read_csv(jtl_file,
                         low_memory=False,
                         error_bad_lines=False,
                         quoting=csv.QUOTE_NONE,
                         encoding='utf-8')
    except Exception as e:
        err_msg = 'read jtl file error. detail:{e}'.format(e=e)
        LOGGER.error(err_msg)
    if df is None:
        return
    threads = int(jtl_file.split(os.sep)[-1].split('_')[0])
    success, elapsed, latency, sent_bytes, receive_bytes = [df.get(x) for x in
                                                            ['success', 'elapsed', 'Latency', 'sentBytes', 'bytes']]
    samples = df.shape[0]
    error_count = success.value_counts().get(False)
    if not error_count:
        error_count = 0
    error_rate = str(float(error_count / samples) * 100) + '%'
    label = df.loc[0, 'label']
    start_time = df.iat[0, 0]
    end_time = df.iloc[-1, 0]
    last_req_time = df.iat[-1, 1]

    # 如果最后一行数据无效,则取上一行
    i = 1
    while not len(str(end_time)) == 13 and not re.findall('[\d]{13}', str(end_time)):
        i += 1
        end_time = df.iloc[-i, 0]
        last_req_time = df.iat[-i, 1]
        samples -= 1

    if isinstance(start_time, str):
        start_time = int(start_time)
    if isinstance(end_time, str):
        end_time = int(end_time)

    local_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time / 1000))
    local_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time / 1000))

    durations = (end_time + last_req_time - start_time) / 1000
    throughput = samples / durations

    report_list = [label, local_start_time, local_end_time, durations, threads, throughput, error_rate,
                   elapsed.min(), elapsed.max(), elapsed.mean(), samples, sent_bytes.mean(), receive_bytes.mean(),
                   latency.mean(), latency.min(), latency.max()]

    return report_list
