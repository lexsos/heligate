from django.conf import settings


CONFIG = {
    'LDAP_DOMAIN': '',
    'LDAP_TREE': '',
    'INET_GROPUT': '',
    'DEFAULT_GROUP': '',
    'DEFAULT_IP4': 1,
    'PRIORITY': 50,
}

CONFIG.update(getattr(settings, 'ACCOUNTS_LDAP', {}))
