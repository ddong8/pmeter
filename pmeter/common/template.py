#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/11 9:24
# @File    : template.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

"""
copy files to cwd dir.
"""

import os
import shutil
import time

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Template(object):
    """
    copy template file to dest dir.
    """

    def __init__(self, name):
        self.top_dir = os.path.join(os.getcwd(), name)
        os.makedirs(self.top_dir, exist_ok=True)
        self.copy_files()

    @staticmethod
    def app_str():
        app_str = """\
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : {time}
# @File    : app.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

import sys

from jty_performance.common.command import execute_from_command_line


def main():
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()\
""".format(time=time.strftime('%Y/%m/%d %H:%M', time.localtime()))

        return app_str

    def copy_files(self):
        prefix_length = len(template_dir) + 1

        # generate app.py file.
        app_file = os.path.join(os.path.dirname(self.top_dir), 'app.py')
        with open(app_file, 'w') as f:
            f.write(self.app_str())

        # copy code and data file.
        for root, dirs, files in os.walk(template_dir):
            path_rest = root[prefix_length:]
            relative_dir = path_rest
            if relative_dir:
                target_dir = os.path.join(self.top_dir, relative_dir)
                os.makedirs(target_dir, exist_ok=True)

            for dirname in dirs[:]:
                if dirname.startswith('.') or dirname == '__pycache__':
                    dirs.remove(dirname)

            for filename in files:
                if filename.endswith(('.pyo', '.pyc', '.py.class')):
                    continue
                old_path = os.path.join(root, filename)
                new_path = os.path.join(self.top_dir, relative_dir, filename)

                shutil.copyfile(old_path, new_path)
