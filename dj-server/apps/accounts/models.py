from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User


class Ip4Entry(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('ip address'),
        protocol='IPv4',
        unique=True,
    )
    create_date = models.DateTimeField(
        verbose_name=_('create date'),
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        verbose_name=_('update date'),
        auto_now=True,
    )
    priority = models.PositiveIntegerField(
        verbose_name=_('priority'),
        default=0,
    )

    def __unicode__(self):
        return u'{0}:{1}'.format(self.user, self.ip_address)

    class Meta:
        verbose_name_plural = _('ip4 entries items')
        verbose_name = _('ip4 entry item')
        ordering = ['user', '-priority', '-update_date']


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        verbose_name=_('user'),
    )
    full_name = models.CharField(
        verbose_name=_('full name'),
        max_length=255,
        blank=True,
    )
    max_ip4_entry = models.PositiveIntegerField(
        verbose_name=_('max count of ip4 entries'),
        default=1,
    )

    def __unicode__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = _('profiles items')
        verbose_name = _('profile item')
        ordering = ['full_name']
