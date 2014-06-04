{% load firewall %}

#!/bin/bash

#*************************************************
# Сбрасываем настройки

iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# Устанавливаем политики по умолчанию
iptables -P FORWARD DROP

# очищаем правила
ip rule flush
ip rule add from all lookup main pref 32766
ip rule add from all lookup default pref 32767

#*************************************************
# Подгружаем модули трассировки

modprobe nf_conntrack
modprobe nf_conntrack_ftp
modprobe nf_conntrack_irc
modprobe nf_nat
modprobe nf_nat_ftp
modprobe nf_nat_irc

#*************************************************
# создание цепочек

# цепочки с фильтрами для групп
{% for group in group_list %}
    {% firewall_group_filter group %}
{% endfor %}

# цепочка классификатор
iptables -t filter -N group_classifier_a
iptables -t filter -N group_classifier_b
{% firewall_group_classifier 'group_classifier_a' 'group_classifier_b' %}
#*************************************************
# настройка правил проходящего трафика

# Разрешаем прохождение установленых соединений
iptables -t filter -A  FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
# Распределяем трафик по группам
iptables -t filter -A  FORWARD -j group_classifier_a
iptables -t filter -A  FORWARD -j group_classifier_b


# Разрешаем пересылку
echo 1 > /proc/sys/net/ipv4/ip_forward
