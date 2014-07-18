import re
import sys


def normalize_script(script):
    norma = script
    norma = re.sub(u' +', u' ', norma)
    norma = re.sub(u'\n\s*', u'\n', norma)
    norma = re.sub(u'^\s*\n', u'', norma)
    return norma


def has_related_objects(record):
    rel_list = record._meta.get_all_related_objects()
    links = [rel.get_accessor_name() for rel in rel_list]

    for link in links:
        qs = getattr(record, link).all()
        if qs.exists():
            return True
    return False


def console_progrees(total, current, out):
    percentage = (float(current) / total) * 100
    sys.stdout.write("\r%d%%" % percentage)
    sys.stdout.flush()
