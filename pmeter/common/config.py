#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/17 19:13
# @File    : config.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
parse config.ini
"""

import configparser
import os


# read configuration from config file
class Config(object):
    """
    parse .ini file by configparser
    """

    def __init__(self, config):
        if os.path.exists(config):
            self.conf = configparser.ConfigParser()
            self.conf.read(config, encoding='UTF-8')
        else:
            raise FileNotFoundError("'config.ini' not found !")


class InitializeConfig(object):
    """
    automatic find config.ini file on cwd path.
    """

    def __init__(self, base_dir=None):
        if base_dir:
            self.base_dir = base_dir
        else:
            self.base_dir = os.path.join(os.path.dirname(os.getcwd()), 'pmeter')
        self.config_file = None
        self.init_config()

    def init_config(self):
        self.config_file = os.path.join(os.path.join(self.base_dir, "etc"), "config.ini")
        if not os.path.exists(self.config_file):
            self.search_config()

    def search_config(self):
        for root, dirs, files in os.walk(self.base_dir):
            flg = False
            for file in files:
                if file.lower() == 'config.ini':
                    self.base_dir = os.path.dirname(root)
                    self.config_file = os.path.join(root, file)
                    flg = True
                    break
            if flg:
                break


init_config = InitializeConfig()
base_dir = init_config.base_dir
config_file = init_config.config_file

CONF = Config(config=config_file)
CONF = CONF.conf
