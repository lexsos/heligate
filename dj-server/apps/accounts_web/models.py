from django.utils.translation import ugettext_lazy as _
from django.db import models


class RedirectUrl(models.Model):

    url = models.TextField(
        verbose_name=_('page url')
    )
    create_date = models.DateTimeField(
        verbose_name=_('create date'),
        auto_now_add=True,
    )

    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name_plural = _('redirect url items')
        verbose_name = _('redirect url item')
        ordering = ['create_date']
