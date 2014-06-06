# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


def fixture():

    from django.contrib.auth.models import Group
    from accounts_ldap.settings import CONFIG
    group_default = Group(name=CONFIG['DEFAULT_GROUP'])
    group_default.save()

    from django.contrib.auth.models import User
    from accounts.models import Profile
    for user in User.objects.all():
            profile = Profile(user=user, group=group_default)
            profile.save()

    from firewall.models import RuleKit
    from firewall.patterns import ACTION_ALLOW
    rule_kit = RuleKit(group=group_default, default_action=ACTION_ALLOW)
    rule_kit.save()

    from firewall.models import NetInterface
    from firewall.patterns import INTERNAL_IF
    default_if = NetInterface(if_name='eth0', if_type=INTERNAL_IF)
    default_if.save()


class Migration(DataMigration):

    def forwards(self, orm):
        fixture()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {

    }

    complete_apps = ['core']
    symmetrical = True
