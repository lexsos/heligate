#!/usr/bin/env python
import os
import sys


proj_dir = os.path.join(os.path.dirname(__file__), '..')
proj_dir = os.path.normpath(os.path.abspath(proj_dir))

if proj_dir not in sys.path:
    sys.path.insert(0, proj_dir)

os.environ['PYTHONPATH'] = proj_dir
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings.development'

apps_root = os.path.join(proj_dir, 'apps')
if apps_root not in sys.path:
    sys.path.insert(0, apps_root)


from squid3.loger import Loger


if __name__ == '__main__':

    loger = Loger()

    while True:
        line = sys.stdin.readline()
        cmd_type = line[0]
        if cmd_type == 'L':
            loger.log(line)
        elif cmd_type == 'F':
            loger.flush()
