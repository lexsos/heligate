#!/usr/bin/env python
import django_header

from message_bus.event import event_system_start, apply_system_start
from message_bus.event import apply_events
from message_bus.utils import run_events_loop

if __name__ == '__main__':
    event_system_start()
    apply_system_start()

    run_events_loop(apply_events)
