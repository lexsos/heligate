from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from .utils import generate_key


class DynamicAccounts(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
    )
    secret = models.TextField(
        verbose_name=_('secret key'),
        help_text=_('shared secret key'),
        default=generate_key,
    )

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = _('dynamic accounts items')
        verbose_name = _('dynamic account item')
        ordering = ['user', ]
