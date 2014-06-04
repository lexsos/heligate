import os
from subprocess import call


from django.conf import settings

from .models import Event
from .settings import CONFIG
from .patterns import (
    ACCOUNTS_REG_USER,
    ACCOUNTS_UNREG_USER,
)


def add_event(event_id):
    event = Event(event_id=event_id)
    event.save()


def event_reg_user():
    add_event(ACCOUNTS_REG_USER)


def event_unreg_user():
    add_event(ACCOUNTS_UNREG_USER)


def run_scripts(scripts):
    old_cd = os.getcwd()

    rc_root = os.path.join(settings.PROJECT_ROOT, '..', 'rc.d')
    rc_root = os.path.normpath(os.path.abspath(rc_root))

    os.chdir(rc_root)
    for script in scripts:
        path = os.path.join(rc_root, script)
        call(path)
    os.chdir(old_cd)


def apply_events(event_type=None):
    qs = Event.objects.filter(applyed=False)
    if not event_type is None:
        qs = qs.filter(event_id__in=event_type)

    scripts = set()
    for event in qs:
        script_name = CONFIG['EVENTS'][event.event_id]
        scripts |= set([script_name,])

    qs.update(applyed=True)
    run_scripts(scripts)
