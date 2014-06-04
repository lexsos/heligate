from django.utils.translation import ugettext_lazy as _
from django.db import models


class Event(models.Model):

    create_date = models.DateTimeField(
        verbose_name=_('create date'),
        auto_now_add=True,
    )
    event_id = models.IntegerField(
        verbose_name=_('event id'),
    )
    applyed = models.BooleanField(
        verbose_name=_('applyed'),
        default=False,
    )

    def __unicode__(self):
        return u'{0}:{1}'.format(self.create_date, self.event_id)

    class Meta:
        verbose_name_plural = _('events items')
        verbose_name = _('event item')
        ordering = ['create_date']
