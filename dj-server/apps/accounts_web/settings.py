from django.conf import settings


CONFIG = {
    'DEFAULT_GROUP': '',
    'DEFAULT_IP4': 1,
    'PRIORITY': 50,
    'WEB_SCHEME': 'http',

    'LDAP_DOMAIN': '',
    'LDAP_TREE': '',
    'LDAP_INET_GROUPT': '',
    'LDAP_BIND_USER': None,
    'LDAP_BIND_PASSWORD': None,
}

CONFIG.update(getattr(settings, 'ACCOUNTS_WEB', {}))
