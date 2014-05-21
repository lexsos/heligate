from django.conf import settings


CONFIG = {
    'HTTP_PORT': 3129,
    'HTTPS_PORT': 3128,
}

CONFIG.update(getattr(settings, 'ACCOUNTS_DYNAMIC_IP_CONFIG', {}))
