import random

from .settings import CONFIG


def generate_key():
    chars = CONFIG['ALLOW_CHARS']
    klen = CONFIG['KEY_LEN']
    return ''.join([random.SystemRandom().choice(chars) for i in range(klen)])
