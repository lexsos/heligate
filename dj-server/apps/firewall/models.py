from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import Group


IP_VERSION_4 = 'ipv4'
IP_VERSION_6 = 'ipv6'
IP_VERSION = (
    (IP_VERSION_4, _('ip version 4')),
    (IP_VERSION_6, _('ip version 6')),
)

PROTOCOL_TYPE_TCP = 'tcp'
PROTOCOL_TYPE_UDP = 'udp'
PROTOCOL_TYPE_ICMP = 'icmp'
PROTOCOL_TYPE = (
    (PROTOCOL_TYPE_TCP, 'TCP'),
    (PROTOCOL_TYPE_UDP, 'UDP'),
    (PROTOCOL_TYPE_ICMP, 'ICMP'),
)

ICMP_ANY = 'any'
ICMP_ECHO_REP = 'echo-reply'
ICMP_ECHO_REQ = 'echo-request'
ICMP_TYPE = (
    (ICMP_ANY, _('any')),
    (ICMP_ECHO_REP, _('echo reply')),
    (ICMP_ECHO_REQ, _('echo request')),
)

ACTION_DENY = 'deny'
ACTION_ALLOW = 'allow'
ACTION = (
    (ACTION_DENY, _('deny')),
    (ACTION_ALLOW, _('allow')),
)


class IpFilter(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('filter name'),
        unique=True,
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_('description'),
        blank=True,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('ip filters items')
        verbose_name = _('ip filter item')
        ordering = ['name']


class NetInterface(models.Model):

    if_name = models.CharField(
        max_length=255,
        verbose_name=_('interface name'),
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_('description'),
    )

    def __unicode__(self):
        return u'{0}:{1}'.format(self.name, self.description)

    class Meta:
        verbose_name_plural = _('net interfaces items')
        verbose_name = _('net interface item')
        ordering = ['description']


class Classifier(models.Model):

    ip_filter = models.ForeignKey(
        IpFilter,
        verbose_name=_('ip filter'),
    )
    ip_version = models.CharField(
        max_length=255,
        verbose_name=_('ip protocol version'),
        choices=IP_VERSION,
        default=IP_VERSION_4
    )
    protocol = models.CharField(
        max_length=255,
        verbose_name=_('protocol type'),
        choices=PROTOCOL_TYPE,
        default=PROTOCOL_TYPE_TCP
    )
    src_ip = models.CharField(
        max_length=255,
        verbose_name=_('source ip address'),
        blank=True,
    )
    dst_ip = models.CharField(
        max_length=255,
        verbose_name=_('destination ip address'),
        blank=True,
    )
    input_if = models.ForeignKey(
        NetInterface,
        verbose_name=_('input interface'),
        null=True,
        blank=True,
        related_name='+',
    )
    output_if = models.ForeignKey(
        NetInterface,
        verbose_name=_('output interface'),
        null=True,
        blank=True,
        related_name='+',
    )
    src_ports = models.CharField(
        max_length=255,
        verbose_name=_('source ports'),
        blank=True,
    )
    dst_ports = models.CharField(
        max_length=255,
        verbose_name=_('destination ports'),
        blank=True,
    )
    icmp_type = models.CharField(
        max_length=255,
        verbose_name=_('icmp type'),
        blank=True,
        choices=ICMP_TYPE
    )

    def __unicode__(self):
        return u'{0}:{1}'.format(self.ip_version, self.protocol)

    class Meta:
        verbose_name_plural = _('classifieres items')
        verbose_name = _('classifier item')
        ordering = ['ip_filter']


class RuleSet(models.Model):

    group = models.OneToOneField(
        Group,
        verbose_name=_('group'),
    )
    default_action = models.CharField(
        max_length=255,
        choices=ACTION,
        verbose_name=_('default action'),
    )

    def __unicode__(self):
        return u'{0}:{1}'.format(self.group, self.default_action)

    class Meta:
        verbose_name_plural = _('rulesets items')
        verbose_name = _('ruleset item')
        ordering = ['group']


class IpRule(models.Model):

    rule_set = models.ForeignKey(
        RuleSet,
        verbose_name=_('ruleset item'),
    )
    ip_filter = models.ForeignKey(
        IpFilter,
        verbose_name=_('ip filter'),
    )
    action = models.CharField(
        max_length=255,
        choices=ACTION,
        verbose_name=_('action'),
    )
    enabled = models.BooleanField(
        verbose_name=_('enabled'),
        default=True,
    )
    weight = models.PositiveIntegerField(
        verbose_name=_('weight'),
        default=0,
    )

    def __unicode__(self):
        return u'{0}:{1}'.format(
            self.rule_set.group,
            self.ip_filter.name,
            self.action
        )

    class Meta:
        verbose_name_plural = _('iprules items')
        verbose_name = _('iprule item')
        ordering = ['rule_set', '-weight', 'ip_filter']
