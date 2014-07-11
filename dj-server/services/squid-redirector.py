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


from squid3.redirector import Redirector


sig_handled = False


def handler(signum, frame):
    global sig_handled
    sig_handled = True


if __name__ == '__main__':

    signal.signal(signal.SIGUSR1, handler)
    redirector = Redirector()

    while True:

        global sig_handled
        if sig_handled:
            sig_handled = False
            redirector.users_updated()

        line = None
        try:
            line = sys.stdin.readline()
        except IOError:
            continue

        url = redirector.redirect(line)
        sys.stdout.write(url)
        sys.stdout.flush()
