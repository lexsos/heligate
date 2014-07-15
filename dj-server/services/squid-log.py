#!/usr/bin/env python
import django_header
import os
import sys
import threading

from squid3.loger import Loger
from message_bus.utils import run_events_loop
from message_bus.patterns import (
    ACCOUNTS_REG_USER,
    ACCOUNTS_UNREG_USER,
    SYSTEM_START,
    SYSTEM_FULL_RECONFIG,
)

loger = Loger()


def loger_event(events):
    if (ACCOUNTS_REG_USER in events) or (ACCOUNTS_UNREG_USER in events):
        loger.users_updated()
    if (SYSTEM_START in events) or (SYSTEM_FULL_RECONFIG in events):
        loger.config_updated()
    print events


def loop_run():
    try:
        run_events_loop(loger_event)
    except:
        os._exit(1)


if __name__ == '__main__':

    event_loop_thread = threading.Thread(target=loop_run)
    event_loop_thread.start()

    try:
        while True:

            line = sys.stdin.readline()

            cmd_type = line[0]
            if cmd_type == 'L':
                loger.log(line)
            elif cmd_type == 'F':
                loger.flush()
    except:
        os._exit(1)
