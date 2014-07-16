from django.conf import settings
import logging
from  logging.handlers import SysLogHandler


CONFIG = {
    'LOG_NAME': 'heligate',
    'LOG_LEVEL': logging.WARNING,
    'LOG_ADDRESS': '/dev/log',
    'LOG_FORMAT': 'heligate[%(process)d]: [%(levelname)s] %(message)s',
    'LOG_FACILITY': SysLogHandler.LOG_DAEMON,
}

CONFIG.update(getattr(settings, 'HELIGATE', {}))
