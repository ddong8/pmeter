#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-7-18 11:11
# @File    : logger.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
initialize logger
"""

import logging
import os

from pmeter.common import const


def initialize_logger():
    """
    initialize log config
    :return: None
    """
    logging.getLogger().setLevel(level=logging.INFO)
    handler = logging.FileHandler(filename=os.path.join(const.LOG_DIR, const.CONF.get("Log", "LOG_PATH")))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logging.getLogger().addHandler(handler)
