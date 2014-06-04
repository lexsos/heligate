iptables -t filter -F {{ chain_a }}
{% for ip4 in ip4_list %}
    iptables -t filter -A {{ chain_a }} --src {{ ip4.ip_address }} -j group{{ ip4.user.profile.group.pk }}
    iptables -t filter -A {{ chain_a }} --dst {{ ip4.ip_address }} -j group{{ ip4.user.profile.group.pk }}
{% endfor %}

iptables -t filter -F {{ chain_b }}
{% for ip4 in ip4_list %}
    iptables -t filter -A {{ chain_b }} --src {{ ip4.ip_address }} -j group{{ ip4.user.profile.group.pk }}
    iptables -t filter -A {{ chain_b }} --dst {{ ip4.ip_address }} -j group{{ ip4.user.profile.group.pk }}
{% endfor %}
