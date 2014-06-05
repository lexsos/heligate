# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

from event_log.utils import event_reg_user, event_unreg_user
from .models import Ip4Entry, Profile


def user_reg_ip4(user, ip_address, priority=0):
    # Проверим активен ли пользователь
    if not user.is_active:
        return 1
    # если уже есть запись с таким пользователем и ip адресом
    entries = Ip4Entry.objects.filter(user=user, ip_address=ip_address)
    if entries.exists():
        entry = entries[0]
        # Приоритет можно только повышать
        entry.priority = max(priority, entry.priority)
        entry.save()
        return 0
    else:
        # если ip адрес числится на комто другом
        entries = Ip4Entry.objects.filter(ip_address=ip_address)
        if entries.exists():
            # если у существующей записи приоритет выше то вытеснять нельзя
            if entries[0].priority > priority:
                return 1
            entries.delete()
            event_unreg_user()


        # проверяем превышение количества записей у текущего пользователя
        entries = Ip4Entry.objects.filter(user=user)
        current_count = entries.count()
        max_count = user.profile.max_ip4_entry
        if current_count >= max_count:
            to_del_count = current_count - max_count + 1
            entries = Ip4Entry.objects.filter(user=user)
            entries = entries.filter(priority__lte=priority)
            entries = entries.order_by('priority', 'update_date')
            if to_del_count > entries.count():
                return 1
            else:
                for entry in entries[:to_del_count]:
                    entry.delete()
                event_unreg_user()

        # привязываем ip адресс к пользователю
        entries = Ip4Entry(
            user=user,
            ip_address=ip_address,
            priority=priority,
        )
        entries.save()
        event_reg_user()
        return 0


def user_unreg_ip(user, ip_address=None):
    entries = Ip4Entry.objects.filter(user=user)
    if not ip_address is None:
        entries = entries.filter(ip_address=ip_address)
    entries.delete()
    event_unreg_user()


def create_account(username, max_ip4_entry, group_name, full_name=''):
    new_user = User(username=username, is_active=True)
    new_user.save()

    group = Group.objects.get(name=group_name)
    new_profile = Profile(
        user=new_user,
        full_name=full_name,
        max_ip4_entry=max_ip4_entry,
        group=group
    )
    new_profile.save()

    return new_user


def get_user_by_ip4(ip4):
    try:
        return Ip4Entry.objects.get(ip_address=ip4).user
    except ObjectDoesNotExist:
        return None

