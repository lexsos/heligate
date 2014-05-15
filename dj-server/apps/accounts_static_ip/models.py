from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from accounts.utils import user_reg_ip4
from accounts_static_ip.settings import CONFIG


class StaticIp4(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('ip address'),
        protocol='IPv4',
        unique=True,
    )

    def __unicode__(self):
        return u'{0}:{1}'.format(self.user, self.ip_address)

    def register(self):
            user_reg_ip4(self.user, self.ip_address, CONFIG['PRIORITY'])

    class Meta:
        verbose_name_plural = _('static ip4 items')
        verbose_name = _('static ip4 item')
        ordering = ['user', 'ip_address']
