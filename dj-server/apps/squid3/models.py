from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from firewall.models import ClassifierKit

from .settings import CONFIG


SQUID_PORT = (
    (CONFIG['HTTP_PORT'], 'HTTP'),
    #(CONFIG['HTTPS_PORT'],_('HTTPS')),
)


class ExcludedFilter(models.Model):

    classifier_kit = models.ForeignKey(
        ClassifierKit,
        verbose_name=_('classifier kit item'),
    )
    enabled = models.BooleanField(
        verbose_name=_('enabled'),
        default=True,
    )

    def get_classifiers4(self):
        return self.classifier_kit.get_classifiers_ip4()

    def get_classifiers6(self):
        return self.classifier_kit.get_classifiers_ip6()

    def __unicode__(self):
        return self.classifier_kit.name

    class Meta:
        verbose_name_plural = _('excluded filters items')
        verbose_name = _('excluded filter item')
        ordering = ['classifier_kit']


class ExcludedUser(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        unique=True,
    )

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = _('excluded users items')
        verbose_name = _('excluded user item')
        ordering = ['user']


class InterceptFilter(models.Model):

    classifier_kit = models.ForeignKey(
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

    def get_classifiers4(self):
        return self.classifier_kit.get_classifiers_ip4()

    def get_classifiers6(self):
        return self.classifier_kit.get_classifiers_ip6()

    def __unicode__(self):
        return u'{0}:{1}'.format(self.classifier_kit.name, self.squid_port)

    class Meta:
        verbose_name_plural = _('intercept filters items')
        verbose_name = _('intercept filter item')
        ordering = ['squid_port']
