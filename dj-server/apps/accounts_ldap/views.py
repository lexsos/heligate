from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse
from ipware.ip import get_ip

from accounts.utils import user_reg_ip4, get_user_by_ip4, user_unreg_ip
from event_log.utils import apply_user_reg
from .forms import LdapAuthForm
from .settings import CONFIG
from .models import RedirectUrl


class LdapAuthView(FormView):

    template_name = 'accounts_ldap/auth.html'
    form_class = LdapAuthForm

    def get_url_for_redirect(self):
        pk = self.kwargs.get('pk')
        try:
            redirect_url = RedirectUrl.objects.get(pk=pk)
            return redirect_url.url
        except RedirectUrl.DoesNotExist:
            pass
        return reverse('accounts_ldap_auth')

    def form_valid(self, form):
        user = form.cleaned_data['user']
        ip_address = get_ip(self.request)
        if user_reg_ip4(user, ip_address, CONFIG['PRIORITY']) != 0:
            self.success_url = reverse('accounts_ldap_error')
        else:
            apply_user_reg()
            self.success_url = self.get_url_for_redirect()
        return super(LdapAuthView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LdapAuthView, self).get_context_data(**kwargs)
        ip_address = get_ip(self.request)
        context['proxy_user'] = get_user_by_ip4(ip_address)
        return context


class LogoutView(RedirectView):

    permanent = False

    def get_redirect_url(self):
        ip_address = get_ip(self.request)
        user = get_user_by_ip4(ip_address)
        if (not user is None) and (not ip_address is None):
            user_unreg_ip(user, ip_address)
            apply_user_reg()
        return reverse('accounts_ldap_auth')
