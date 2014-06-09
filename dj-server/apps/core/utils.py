import re


def normalize_script(script):
    norma = script
    norma = re.sub(u' +', u' ', norma)
    norma = re.sub(u'\n\s*', u'\n', norma)
    norma = re.sub(u'^\s*\n', u'', norma)
    return norma
