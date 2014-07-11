from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from .settings import CONFIG


def get_auth_url(user_url):
    from .models import RedirectUrl

    redirect_url = RedirectUrl(url=user_url)
    redirect_url.save()
    pk = redirect_url.pk
    uri = reverse('accounts_web_auth_redirect', kwargs={'pk': pk})
    site = Site.objects.get_current()
    web_scheme = CONFIG['WEB_SCHEME']
    return '{0}://{1}{2}'.format(web_scheme, site, uri)
