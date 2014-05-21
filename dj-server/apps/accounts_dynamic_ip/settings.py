from django.conf import settings


CONFIG = {
    'PRIORITY': 50,
    'KEY_LEN': 128,
    'ALLOW_CHARS': 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)',
}

CONFIG.update(getattr(settings, 'ACCOUNTS_DYNAMIC_IP_CONFIG', {}))
