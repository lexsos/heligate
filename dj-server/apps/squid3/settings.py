from django.conf import settings


CONFIG = {
    'HTTP_PORT': 3129,
    'HTTPS_PORT': 3128,

    'DOMAIN_CACHE_SIZE': 1000,
    'FILTER_CACHE_SIZE': 10000,
    'COUNTER_MUL': 2,

    'SQUID_CONF_FILE': '/etc/squid3/squid.conf',
    'SQUID_DISK_CACHE_SIZE': 5000,
    'SQUID_MEM_CACHE_SIZE': 256,
    'SQUID_MAX_OBJ_SIZE': 100,
    'SQUID_MAX_MEM_OBJ_SIZE': 10,
    'SQUID_REWRITER_COUNT': 5,
    'SQUID_REWRITE_BYPASS': 'off',
    'SQUID_CACHE_DIR': '/var/spool/squid3',
}

CONFIG.update(getattr(settings, 'SQUID3_CONFIG', {}))
