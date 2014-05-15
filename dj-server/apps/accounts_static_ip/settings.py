from django.conf import settings


CONFIG = {
    'PRIORITY': 100,
}

CONFIG.update(getattr(settings, 'ACCOUNTS_STATIC_IP_CONFIG', {}))
