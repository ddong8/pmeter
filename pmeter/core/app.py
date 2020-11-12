#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/10 17:20
# @File    : app.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

from pmeter.common import const
from pmeter.core.jmx_test import SingleInterface
from pmeter.core.report import GenerateReport


class App(object):
    def __init__(self, *args, **kwargs):
        kwargs['conf'] = const.CONF
        self.kwargs = kwargs

    def exe_single_interface(self):
        SingleInterface(**self.kwargs)

    def generate_report(self):
        GenerateReport(**self.kwargs)
