import re
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User, Group

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


class L2Domain(models.Model):

    l2_name = models.CharField(
        verbose_name=_('l2 domain name'),
        max_length=1024,
        unique=True,
    )

    def __unicode__(self):
        return self.l2_name

    class Meta:
        verbose_name_plural = _('l2 domains items')
        verbose_name = _('l2 domain item')
        ordering = ['l2_name']


class Domain(models.Model):

    name = models.CharField(
        verbose_name=_('domain name'),
        max_length=1024,
        unique=True,
    )
    l2_domain = models.ForeignKey(
        L2Domain,
        verbose_name=_('l2 domain item'),
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('domains items')
        verbose_name = _('domain item')
        ordering = ['name']


class SquidLog(models.Model):

    access_date = models.DateTimeField(
        verbose_name=_('access date'),
        auto_now_add=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        null=True,
        blank=True,
    )
    domain = models.ForeignKey(
        Domain,
        verbose_name=_('domain item'),
    )
    url = models.TextField(
        verbose_name=_('page url')
    )
    size = models.IntegerField(
        verbose_name=_('object size')
    )

    def __unicode__(self):
        return u'{0}:{1}'.format(self.access_date, self.domain.name)

    class Meta:
        verbose_name_plural = _('squid log items')
        verbose_name = _('squid log item')
        ordering = ['access_date']


class DomainClassifierKit(models.Model):

    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        unique=True,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('domain classifier kit items')
        verbose_name = _('domain classifier kit item')
        ordering = ['name']


class DomainClassifier(models.Model):

    classifier_kit = models.ForeignKey(
        DomainClassifierKit,
        verbose_name=_('domain classifier kit item'),
    )
    l2_domain = models.ForeignKey(
        L2Domain,
        verbose_name=_('l2 domain item'),
        blank=True,
        null=True,
    )
    domain = models.ForeignKey(
        Domain,
        verbose_name=_('domain item'),
        blank=True,
        null=True,
    )
    reg_expr = models.CharField(
        verbose_name=_('regular expression'),
        max_length=255,
        blank=True,
    )

    def is_matched(self, domain):
        if self.l2_domain:
            return domain.l2_domain == self.l2_domain
        elif self.domain:
            return domain == self.domain
        elif self.reg_expr:
            return not (re.match(self.reg_expr, domain.name) is None)
        return False

    def __unicode__(self):
        if self.l2_domain:
            return unicode(self.l2_domain)
        elif self.domain:
            return unicode(self.domain)
        elif self.reg_expr:
            return unicode(self.reg_expr)
        return _('empty')

    class Meta:
        verbose_name_plural = _('domain classifier items')
        verbose_name = _('domain classifier item')
        ordering = ['classifier_kit']


class FakeClassifier(object):

    def __init__(self):
        super(FakeClassifier, self).__init__()

    def is_matched(self, domain):
        return True

    def __unicode__(self):
        return u'FakeClassifier'


class DomainFilterKit(models.Model):

    group = models.OneToOneField(
        Group,
        verbose_name=_('group'),
    )
    default_allow = models.BooleanField(
        verbose_name=_('default allow'),
        default=True,
    )

    def get_filters(self):
        all_filters = []
        for filters in self.domainfilter_set.all():
            all_filters.extend(filters.get_filters())
        all_filters.append((FakeClassifier(), self.default_allow))
        return all_filters

    def __unicode__(self):
        return u'{0}:{1}'.format(self.group, self.default_allow)

    class Meta:
        verbose_name_plural = _('domain filter kit items')
        verbose_name = _('domain filter kit item')
        ordering = ['group']


class DomainFilter(models.Model):

    classifier_kit = models.ForeignKey(
        DomainClassifierKit,
        verbose_name=_('domain classifier kit item'),
    )
    domain_filter_kit = models.ForeignKey(
        DomainFilterKit,
        verbose_name=_('domain filter kit item'),
    )
    allow = models.BooleanField(
        verbose_name=_('allow'),
        default=True,
    )
    weight = models.PositiveIntegerField(
        verbose_name=_('weight'),
        default=0,
    )

    def get_filters(self):
        classifies = self.classifier_kit.domainclassifier_set.all()
        return [(c, self.allow) for c in classifies]

    def __unicode__(self):
        return u'{0}:{1}:{2}'.format(
            self.domain_filter_kit,
            self.classifier_kit,
            self.allow,
        )

    class Meta:
        verbose_name_plural = _('domain filter items')
        verbose_name = _('domain filter item')
        ordering = ['domain_filter_kit', '-weight']
