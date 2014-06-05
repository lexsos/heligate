from django import template
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup


register = template.Library()


@register.filter
def add_class(html, css_class):
    soup = BeautifulSoup(unicode(html), 'html.parser')

    for tag in soup.children:
        if tag.name != 'script':
            if 'class' in tag:
                tag['class'].append(css_class)
            else:
                tag['class'] = [css_class]

    return mark_safe(soup.renderContents())
