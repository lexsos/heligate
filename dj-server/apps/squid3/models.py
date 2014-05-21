from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from firewall.models import ClassifierKit

from .settings import CONFIG


SQUID_PORT = (
    (CONFIG['HTTP_PORT'], 'HTTP'),
    #(CONFIG['HTTPS_PORT'],_('HTTPS')),
)


class InterceptFilter(models.Model):

    classifier = models.ForeignKey(
        ClassifierKit,
        verbose_name=_('classifier kit item'),
    )
    squid_port = models.IntegerField(
        verbose_name=_('squid port'),
        choices=SQUID_PORT,
        default=CONFIG['HTTP_PORT'],
    )
    enabled = models.BooleanField(
        verbose_name=_('enabled'),
        default=True,
    )

    def __unicode__(self):
        return u'{0}:{1}'.format(self.classifier.name, self.squid_port)

    class Meta:
        verbose_name_plural = _('intercept filters items')
        verbose_name = _('intercept filter item')
        ordering = ['squid_port']


class ExcludeUser(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        unique=True,
    )

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = _('exclude users items')
        verbose_name = _('exclude user item')
        ordering = ['user']
