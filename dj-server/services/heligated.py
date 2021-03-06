#!/usr/bin/env python
import django_header

import sys
import os
import signal
import pika
import time
from optparse import OptionParser

from message_bus.event import (
    event_system_start,
    event_system_stop,
    apply_system_start,
    apply_system_stop,
)
from message_bus.event import apply_events
from message_bus.utils import run_events_loop
from core.log import except_hook, logger
from core.daemon import Daemon


running = True


class Heligated(Daemon):

    def run(self):

        logger.info('starting heligated')

        event_system_start()
        apply_system_start()

        logger.info('heligated started')

        global running
        wait_timer = 0
        while running:
            try:
                logger.info('try connect to rabbitmq server')
                time.sleep(wait_timer)
                run_events_loop(apply_events)
            except pika.exceptions.ConnectionClosed:
                wait_timer = 0
                logger.info('rabbitmq connection closed')
            except pika.exceptions.AMQPConnectionError:
                logger.info("can't connect to rabbitmq server")
            except AttributeError:
                pass
            except KeyboardInterrupt:
                running = False

            if wait_timer < 1000:
                wait_timer += 1

        event_system_stop()
        apply_system_stop()

        logger.info('heligated stoped')


def sig_handler(signum, frame):
    global running
    if running:
        running = False
        logger.debug('heligated caught siglan {0}'.format(signum))
        logger.info('heligated stopping')
        os.exit(0)


def get_args():
    parser = OptionParser()
    parser.add_option(
        '-a',
        '--action',
        help='[stop | start | interactive]',
        choices=['stop', 'start', 'interactive'],
        action='store',
    )

    return parser.parse_args()

if __name__ == '__main__':

    sys.excepthook = except_hook
    signal.signal(signal.SIGTERM, sig_handler)

    heligated = Heligated('/var/run/heligate/heligated.pid')
    (options, args) = get_args()

    if options.action == 'start':
        heligated.start()
    elif options.action == 'stop':
        heligated.stop()
    elif options.action == 'interactive':
        heligated.run()
