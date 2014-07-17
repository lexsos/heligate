#!/usr/bin/env python
import django_header
import os
import sys
import threading
import signal

from squid3.logger import Logger
from message_bus.utils import run_events_loop
from message_bus.patterns import (
    ACCOUNTS_REG_USER,
    ACCOUNTS_UNREG_USER,
    SYSTEM_START,
    SYSTEM_FULL_RECONFIG,
)
from core.log import logger
from core.log import except_hook


squid3_logger = Logger()


def logger_event(events):
    if (ACCOUNTS_REG_USER in events) or (ACCOUNTS_UNREG_USER in events):
        squid3_logger.users_updated()
    if (SYSTEM_START in events) or (SYSTEM_FULL_RECONFIG in events):
        squid3_logger.config_updated()


def loop_run():
    try:
        run_events_loop(logger_event)
    except:
        logger.exception('error in squid3 logger')
        os._exit(1)


def sig_handler(signum, frame):
    logger.debug('squid3 logger caught siglan {0}'.format(signum))


if __name__ == '__main__':

    logger.info('squid3 logger starting')
    sys.excepthook = except_hook

    signal.signal(signal.SIGTERM, sig_handler)

    event_loop_thread = threading.Thread(target=loop_run)
    event_loop_thread.start()

    logger.info('squid3 logger started')
    try:
        while True:
            line = sys.stdin.readline()
            cmd_type = line[0]
            if cmd_type == 'L':
                squid3_logger.log(line)
            elif cmd_type == 'F':
                squid3_logger.flush()
    except (IOError, KeyboardInterrupt):
        logger.info('squid3 logger stopping')
        squid3_logger.log_statistic()
        logger.info('squid3 logger stoped')
        os._exit(0)
    except:
        logger.exception('error in squid3 logger')
        os._exit(1)
