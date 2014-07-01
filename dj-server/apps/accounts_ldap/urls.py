from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import LdapAuthView, LogoutView


urlpatterns = patterns(
    '',
    url(
        r'^$',
        LdapAuthView.as_view(),
        name='accounts_ldap_auth',
    ),
    url(
        r'^(?P<pk>\d+)/$',
        LdapAuthView.as_view(),
        name='accounts_ldap_auth_redirect',
    ),
    url(
        r'^logout/$',
        LogoutView.as_view(),
        name='accounts_ldap_logout',
    ),
    url(
        r'^error/$',
        TemplateView.as_view(template_name='accounts_ldap/error.html'),
        name='accounts_ldap_error',
    ),
)
