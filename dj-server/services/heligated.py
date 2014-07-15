#!/usr/bin/env python
import os
import sys
import signal


proj_dir = os.path.join(os.path.dirname(__file__), '..')
proj_dir = os.path.normpath(os.path.abspath(proj_dir))

if proj_dir not in sys.path:
    sys.path.insert(0, proj_dir)

os.environ['PYTHONPATH'] = proj_dir
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings.development'

apps_root = os.path.join(proj_dir, 'apps')
if apps_root not in sys.path:
    sys.path.insert(0, apps_root)


from message_bus.configurator import run
from message_bus.event import event_system_start, apply_system_start

if __name__ == '__main__':
    event_system_start()
    apply_system_start()

    run()

