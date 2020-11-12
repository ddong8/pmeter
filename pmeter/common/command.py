#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/24 14:12
# @File    : command.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
execute commands.
"""
import argparse
import sys

from pmeter.common.template import Template

parser = argparse.ArgumentParser(description='jmeter auto test tool.')
parser.add_argument('init', help='initialize project.')
parser.add_argument('restart', help='restart slave jmeter server.')
parser.add_argument('distribute', help='distribute csv config file.')
parser.add_argument('auto_exe', help='execute single jmeter test.')
parser.add_argument('report', help='generate report.')


def execute_init():
    """
    execute initialize project.
    :return: None
    """
    if len(sys.argv) >= 3:
        name = sys.argv[2]
    else:
        name = 'pmeter'
    Template(name)


def execute_from_command_line(args=None):
    """
    parse command parmas from sys.argv.
    :param args: list --> sys.argv
    :return: None
    """
    args = args or sys.argv[:]

    try:
        sub_command = args[1]
    except IndexError:
        sub_command = 'help'  # display help if no arguments were given.

    sub_command = sub_command.lower()
    cmd_list = ['init', 'restart', 'distribute', 'auto_exe', 'report']

    if sub_command not in cmd_list:
        sub_command = 'help'

    if sub_command in ['help', '-h', '--help']:
        parser.parse_args(['-h'])
        return
    elif sub_command == 'init':
        execute_init()
    else:
        cmd_list.pop(0)
        from pmeter.common.action import execute_actions
        execute_actions(sub_command, cmd_list)
