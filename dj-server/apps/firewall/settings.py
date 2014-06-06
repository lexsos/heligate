from django.conf import settings


CONFIG = {
    'DIVERT_MARK': 1000,
    'DIVERT_ROUTE_TABLE': 100,
}

CONFIG.update(getattr(settings, 'FIREWALL_CONFIG', {}))
