from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import WebAuthView, LogoutView


urlpatterns = patterns(
    '',
    url(
        r'^$',
        WebAuthView.as_view(),
        name='accounts_web_auth',
    ),
    url(
        r'^(?P<pk>\d+)/$',
        WebAuthView.as_view(),
        name='accounts_web_auth_redirect',
    ),
    url(
        r'^logout/$',
        LogoutView.as_view(),
        name='accounts_web_logout',
    ),
    url(
        r'^error/$',
        TemplateView.as_view(template_name='accounts_web/error.html'),
        name='accounts_web_error',
    ),
)
