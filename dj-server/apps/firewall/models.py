from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import Group

from .patterns import (
    IP_VERSION_4, IP_VERSION_6,
    PROTOCOL_TYPE_TCP, PROTOCOL_TYPE_UDP, PROTOCOL_TYPE_ICMP,
    ICMP_ANY, ICMP_ECHO_REP, ICMP_ECHO_REQ,
    ACTION_DENY, ACTION_ALLOW,
    INTERNAL_IF, EXTERNAL_IF,
)
from .utils import get_ipt_params


IP_VERSION = (
    (IP_VERSION_4, _('ip version 4')),
    (IP_VERSION_6, _('ip version 6')),
)
PROTOCOL_TYPE = (
    (PROTOCOL_TYPE_TCP, 'TCP'),
    (PROTOCOL_TYPE_UDP, 'UDP'),
    (PROTOCOL_TYPE_ICMP, 'ICMP'),
)
ICMP_TYPE = (
    (ICMP_ANY, _('any')),
    (ICMP_ECHO_REP, _('echo reply')),
    (ICMP_ECHO_REQ, _('echo request')),
)
ACTION = (
    (ACTION_DENY, _('deny')),
    (ACTION_ALLOW, _('allow')),
)

INTERFACE_TYPE = (
    (INTERNAL_IF, _('internal')),
    (EXTERNAL_IF, _('external')),
)


class ClassifierKit(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('classifier kit name'),
        unique=True,
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_('description'),
        blank=True,
    )

    def get_classifiers_ip4(self):
        return self.classifier_set.filter(ip_version=IP_VERSION_4)

    def get_classifiers_ip6(self):
        return self.classifier_set.filter(ip_version=IP_VERSION_6)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('classifier kits items')
        verbose_name = _('classifier kit item')
        ordering = ['name']


class NetInterface(models.Model):

    if_name = models.CharField(
        max_length=255,
        verbose_name=_('interface name'),
    )
    if_type = models.CharField(
        max_length=255,
        verbose_name=_('interface type'),
        choices=INTERFACE_TYPE,
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_('description'),
        blank=True,
    )

    def __unicode__(self):
        return u'{0}:{1}'.format(self.if_name, self.description)

    class Meta:
        verbose_name_plural = _('net interfaces items')
        verbose_name = _('net interface item')
        ordering = ['description']


class Classifier(models.Model):

    classifier_kit = models.ForeignKey(
        ClassifierKit,
        verbose_name=_('classifier kit item'),
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
        default=PROTOCOL_TYPE_TCP,
        blank=True,
    )
    src_ip = models.CharField(
        max_length=255,
        verbose_name=_('source ip address'),
        blank=True,
    )
    src_ip_not = models.BooleanField(
        verbose_name=_('negation source ip address'),
        default=False,
    )
    dst_ip = models.CharField(
        max_length=255,
        verbose_name=_('destination ip address'),
        blank=True,
    )
    dst_ip_not = models.BooleanField(
        verbose_name=_('negation destination ip address'),
        default=False,
    )
    input_if = models.ForeignKey(
        NetInterface,
        verbose_name=_('input interface'),
        null=True,
        blank=True,
        related_name='+',
    )
    input_if_not = models.BooleanField(
        verbose_name=_('negation input interface'),
        default=False,
    )
    output_if = models.ForeignKey(
        NetInterface,
        verbose_name=_('output interface'),
        null=True,
        blank=True,
        related_name='+',
    )
    output_if_not = models.BooleanField(
        verbose_name=_('negation output interface'),
        default=False,
    )
    src_ports = models.CharField(
        max_length=255,
        verbose_name=_('source ports'),
        blank=True,
    )
    src_ports_not = models.BooleanField(
        verbose_name=_('negation source ports'),
        default=False,
    )
    dst_ports = models.CharField(
        max_length=255,
        verbose_name=_('destination ports'),
        blank=True,
    )
    dst_ports_not = models.BooleanField(
        verbose_name=_('negation destination ports'),
        default=False,
    )
    icmp_type = models.CharField(
        max_length=255,
        verbose_name=_('icmp type'),
        blank=True,
        choices=ICMP_TYPE
    )

    def iptables_params(self):
        return get_ipt_params(self)

    def __unicode__(self):
        return u'{0}:{1}'.format(self.ip_version, self.protocol)

    class Meta:
        verbose_name_plural = _('classifieres items')
        verbose_name = _('classifier item')
        ordering = ['classifier_kit']


class RuleKit(models.Model):

    group = models.OneToOneField(
        Group,
        verbose_name=_('group'),
    )
    default_action = models.CharField(
        max_length=255,
        choices=ACTION,
        verbose_name=_('default action'),
        blank=True,
    )

    def get_rules(self):
        return self.iprule_set.filter(enabled=True)

    def __unicode__(self):
        return u'{0}:{1}'.format(self.group, self.default_action)

    class Meta:
        verbose_name_plural = _('rule kits items')
        verbose_name = _('rule kit item')
        ordering = ['group']


class IpRule(models.Model):

    rule_kit = models.ForeignKey(
        RuleKit,
        verbose_name=_('rule kit item'),
    )
    classifier_kit = models.ForeignKey(
        ClassifierKit,
        verbose_name=_('classifier kit item'),
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

    def get_classifiers4(self):
        return self.classifier_kit.get_classifiers_ip4()

    def get_classifiers6(self):
        return self.classifier_kit.get_classifiers_ip6()

    def __unicode__(self):
        return u'{0}:{1}'.format(
            self.rule_kit.group,
            self.classifier_kit.name,
            self.action
        )

    class Meta:
        verbose_name_plural = _('iprules items')
        verbose_name = _('iprule item')
        ordering = ['rule_kit', '-weight', 'classifier_kit']
