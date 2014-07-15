from django.conf import settings
from .patterns import (
    SYSTEM_START,
    ACCOUNTS_REG_USER,
    ACCOUNTS_UNREG_USER,
)


EVENTS = {
    SYSTEM_START: 'start.sh',
    ACCOUNTS_REG_USER: 'connects-update.sh',
    ACCOUNTS_UNREG_USER: 'connects-update.sh',
}


CONFIG = {
    'EVENTS': EVENTS,
    'RABBIT_HOST': 'localhost',
    'RABBIT_EXCHANGE': 'hiligate.events',
}


CONFIG.update(getattr(settings, 'MESSAGE_BUS', {}))
