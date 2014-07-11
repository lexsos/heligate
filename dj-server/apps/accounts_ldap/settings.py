from django.conf import settings


CONFIG = {
    'LDAP_DOMAIN': '',
    'LDAP_TREE': '',
    'LDAP_INET_GROPUT': '',
    'DEFAULT_GROUP': '',
    'DEFAULT_IP4': 1,
    'PRIORITY': 50,
    'WEB_SCHEME': 'http',
}

CONFIG.update(getattr(settings, 'ACCOUNTS_LDAP', {}))
