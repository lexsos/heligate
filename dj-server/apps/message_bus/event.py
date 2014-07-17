import json

from .models import Event
from .settings import CONFIG
from .utils import run_scripts, rabbit_send
from .patterns import (
    SYSTEM_START,
    ACCOUNTS_REG_USER,
    ACCOUNTS_UNREG_USER,
)

###############################################
# Event system:
# * First, events are added and stored in DB
# * Then, events are confirmed and message
#   about that are sending by bus to
#   another processes
# * And finally, events are applyed by
#   heligated.  Heligated run proper scripts
#   and change events status in DB to applyed.
###############################################


# Adding events functions
def add_event(event_id):
    event = Event(event_id=event_id)
    event.save()


def event_system_start():
    add_event(SYSTEM_START)


def event_reg_user():
    add_event(ACCOUNTS_REG_USER)


def event_unreg_user():
    add_event(ACCOUNTS_UNREG_USER)


# Confirm events functions
def confirm_events(event_types):
    qs = Event.objects.filter(applyed=False)
    if not event_types is None:
        qs = qs.filter(event_id__in=event_types)
    qs = qs.order_by('event_id')
    events = qs.values_list('event_id').distinct()
    events = [x[0] for x in events]

    message = json.dumps({'events': events})
    rabbit_send(message)


def confirm_user_reg():
    confirm_events([ACCOUNTS_REG_USER, ACCOUNTS_UNREG_USER])


def confirm_system_start():
    confirm_events([SYSTEM_START])


# Apply events functions
def apply_events(event_type=None):
    qs = Event.objects.filter(applyed=False)
    if not event_type is None:
        qs = qs.filter(event_id__in=event_type)

    scripts = set()
    for event in qs:
        script_name = CONFIG['EVENTS'][event.event_id]
        scripts |= set([script_name, ])

    qs.update(applyed=True)
    run_scripts(scripts)


def apply_user_reg():
    apply_events([ACCOUNTS_REG_USER, ACCOUNTS_UNREG_USER])


def apply_system_start():
    apply_events([SYSTEM_START])
