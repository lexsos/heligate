import logging
import logging.handlers

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
