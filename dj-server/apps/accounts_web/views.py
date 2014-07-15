from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse
from ipware.ip import get_ip

from accounts.utils import user_reg_ip4, get_user_by_ip4, user_unreg_ip
from message_bus.event import confirm_user_reg
from .forms import LdapAuthForm
from .settings import CONFIG
from .models import RedirectUrl


class LogoutView(RedirectView):

    permanent = False

    def get_redirect_url(self):

        ip_address = get_ip(self.request)
        user = get_user_by_ip4(ip_address)
        if (not user is None) and (not ip_address is None):
            user_unreg_ip(user, ip_address)
            confirm_user_reg()

        return reverse('accounts_web_auth')


class LdapAuthView(FormView):

    template_name = 'accounts_web/auth.html'
    form_class = LdapAuthForm

    def get_user_url(self):
        pk = self.kwargs.get('pk')
        try:
            redirect_url = RedirectUrl.objects.get(pk=pk)
            return redirect_url.url
        except RedirectUrl.DoesNotExist:
            return None

    def get_url_for_redirect(self):
        user_url = self.get_user_url()
        if not user_url is None:
            return user_url
        return reverse('accounts_web_auth')

    def form_valid(self, form):
        user = form.cleaned_data['user']
        ip_address = get_ip(self.request)

        if user_reg_ip4(user, ip_address, CONFIG['PRIORITY']) != 0:
            self.success_url = reverse('accounts_web_error')
        else:
            confirm_user_reg()
            self.success_url = self.get_url_for_redirect()
        return super(LdapAuthView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LdapAuthView, self).get_context_data(**kwargs)
        ip_address = get_ip(self.request)
        context['proxy_user'] = get_user_by_ip4(ip_address)
        context['user_url'] = self.get_user_url()
        return context
