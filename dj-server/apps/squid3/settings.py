from django.conf import settings


CONFIG = {
    'HTTP_PORT': 3129,
    'HTTPS_PORT': 3128,
    'DOMAIN_CACHE_SIZE': 1000,
    'COUNTER_MUL': 2,
}

CONFIG.update(getattr(settings, 'SQUID3_CONFIG', {}))
