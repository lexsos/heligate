from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(
        r'^deny/$',
        TemplateView.as_view(template_name='squid3/deny.html'),
        name='squi3_deny',
    ),
)
