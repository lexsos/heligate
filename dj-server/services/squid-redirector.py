#!/usr/bin/env python
import django_header
import os
import sys
import threading

from squid3.redirector import Redirector
from message_bus.patterns import (
    ACCOUNTS_REG_USER,
    ACCOUNTS_UNREG_USER,
    SYSTEM_START,
    SYSTEM_FULL_RECONFIG,
)
from message_bus.utils import run_events_loop


redirector = Redirector()


def redirector_event(events):
    if (ACCOUNTS_REG_USER in events) or (ACCOUNTS_UNREG_USER in events):
        redirector.users_updated()
    if (SYSTEM_START in events) or (SYSTEM_FULL_RECONFIG in events):
        redirector.config_updated()


def loop_run():
    try:
        run_events_loop(redirector_event)
    except:
        os._exit(1)


if __name__ == '__main__':

    event_loop_thread = threading.Thread(target=loop_run)
    event_loop_thread.start()

    try:
        while True:
            line = sys.stdin.readline()
            if len(line) <= 1:
                exit(0)
            url = redirector.redirect(line)
            sys.stdout.write(url)
            sys.stdout.flush()
    except:
        os._exit(1)


#import pdb, sys, traceback
#def except_hook(exctype, value, traceback1):
#    f = open('/tmp/squid.log', 'w')
#    f.write(str(exctype))
#    f.write('\n')
#    traceback.print_tb(traceback1, file=f)
#    f.close()
#    sys.__excepthook__(exctype, value, traceback)
#
#
#sys.excepthook = except_hook
