from django.conf.urls import patterns, url

from .views import LdapAuthView, LogoutView


urlpatterns = patterns('',
    url(
        r'^$',
        LdapAuthView.as_view(),
        name='accounts_ldap_auth',
    ),
    url(
        r'^logout/$',
        LogoutView.as_view(),
        name='accounts_ldap_logout',
    ),
)
