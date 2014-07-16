#!/usr/bin/env python
import django_header
import os
import sys
import threading

from squid3.logger import Logger
from message_bus.utils import run_events_loop
from message_bus.patterns import (
    ACCOUNTS_REG_USER,
    ACCOUNTS_UNREG_USER,
    SYSTEM_START,
    SYSTEM_FULL_RECONFIG,
)


squid3_logger = Logger()


def logger_event(events):
    if (ACCOUNTS_REG_USER in events) or (ACCOUNTS_UNREG_USER in events):
        squid3_logger.users_updated()
    if (SYSTEM_START in events) or (SYSTEM_FULL_RECONFIG in events):
        squid3_logger.config_updated()
    print events


def loop_run():
    try:
        run_events_loop(logger_event)
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
                squid3_logger.log(line)
            elif cmd_type == 'F':
                squid3_logger.flush()
    except:
        os._exit(1)
