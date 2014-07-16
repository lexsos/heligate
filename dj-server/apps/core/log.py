import logging
import logging.handlers
import traceback
import sys

from .settings import CONFIG


formatter = logging.Formatter(CONFIG['LOG_FORMAT'])

syslog_handler = logging.handlers.SysLogHandler(
    address=CONFIG['LOG_ADDRESS'],
    facility=CONFIG['LOG_FACILITY'],
)
syslog_handler.setFormatter(formatter)

logger = logging.getLogger(CONFIG['LOG_NAME'])
logger.setLevel(CONFIG['LOG_LEVEL'])
logger.addHandler(syslog_handler)


def except_hook(exctype, value, tb):
    logger.error(str(exctype))
    msgs = traceback.format_tb(tb)
    for msg in msgs:
        logger.error(msg)
    sys.__excepthook__(exctype, value, tb)
