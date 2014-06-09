ipset --flush squid3_excluded_a

{% for ip4 in ip4_list %}
    ipset --add squid3_excluded_a {{ ip4 }}
{% endfor %}


ipset --flush squid3_excluded_b

{% for ip4 in ip4_list %}
    ipset --add squid3_excluded_b {{ ip4 }}
{% endfor %}
