from django.conf.urls import patterns, url

from .views import AuthView


urlpatterns = patterns(
    '',
    url(
        r'^auth$',
        AuthView.as_view(),
        name='accounts_dynamic_api_auth',
    ),
)
