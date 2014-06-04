from django.conf import settings
from .patterns import (
    ACCOUNTS_REG_USER,
    ACCOUNTS_UNREG_USER,
)


EVENTS = {
    ACCOUNTS_REG_USER: 'connects-update.sh',
    ACCOUNTS_UNREG_USER: 'connects-update.sh',
}


CONFIG = {
    'EVENTS': EVENTS,
}


CONFIG.update(getattr(settings, 'EVENT_LOG', {}))
