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
from core.log import logger
from core.log import except_hook


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
        logger.exception('error in rederector')
        os._exit(1)


if __name__ == '__main__':

    logger.info('rederector starting')
    sys.excepthook = except_hook

    event_loop_thread = threading.Thread(target=loop_run)
    event_loop_thread.start()

    logger.info('rederector started')
    try:
        while True:
            line = sys.stdin.readline()
            if len(line) <= 1:
                logger.debug('rederector received blank line')
                logger.info('rederector stopping')
                redirector.log_statistic()
                logger.info('rederector stoped')
                os._exit(0)
            url = redirector.redirect(line)
            sys.stdout.write(url)
            sys.stdout.flush()
    except KeyboardInterrupt:
        os._exit(0)
    except:
        logger.exception('error in rederector')
        os._exit(1)
