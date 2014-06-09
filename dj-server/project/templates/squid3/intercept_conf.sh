ipset --destroy squid3_excluded_a
ipset --create squid3_excluded_a iphash
ipset --flush squid3_excluded_a

ipset --destroy squid3_excluded_b
ipset --create squid3_excluded_b iphash
ipset --flush squid3_excluded_b

iptables -t mangle -N SQUID3

{% for excluded_filter in excluded_filter_list %}
    {% for classifier in excluded_filter.get_classifiers4 %}
        iptables -t mangle -A SQUID3 {{ classifier.iptables_params }} -j RETURN
    {% endfor %}
{% endfor %}

iptables -t mangle -A SQUID3 -m set --set squid3_excluded_a src -j RETURN
iptables -t mangle -A SQUID3 -m set --set squid3_excluded_b src -j RETURN

{% for intercept_filter in intercept_filter_list %}
    {% for classifier in intercept_filter.get_classifiers4 %}
        iptables -t mangle -A SQUID3 {{ classifier.iptables_params }} -j TPROXY --tproxy-mark {{ mark }} --on-port {{ intercept_filter.squid_port }}
    {% endfor %}
{% endfor %}

iptables  -t mangle -A PREROUTING -j SQUID3
