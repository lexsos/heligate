$IPT4 -t filter -F {{ chain_a }}
{% for ip4 in ip4_list %}
    $IPT4 -t filter -A {{ chain_a }} -src {{ ip4.ip_address }} -j group{{ ip4.user.profile.group.pk }}
    $IPT4 -t filter -A {{ chain_a }} -dst {{ ip4.ip_address }} -j group{{ ip4.user.profile.group.pk }}
{% endfor %}

$IPT4 -t filter -F {{ chain_b }}
{% for ip4 in ip4_list %}
    $IPT4 -t filter -A {{ chain_b }} -src {{ ip4.ip_address }} -j group{{ ip4.user.profile.group.pk }}
    $IPT4 -t filter -A {{ chain_b }} -dst {{ ip4.ip_address }} -j group{{ ip4.user.profile.group.pk }}
{% endfor %}
