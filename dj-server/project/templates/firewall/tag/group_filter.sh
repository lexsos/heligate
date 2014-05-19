$IPT4 -t filter -N group{{ group.pk }}

{% for rule in rule_list %}
    {% for classifier in rule.get_classifiers %}
        $IPT4 -t filter -A group{{ group.pk }} {{ classifier.iptables_params }} -j {{ rule.action }}
    {% endfor %}
{% endfor %}

{% if rulset.default_action %}
    $IPT4 -t filter -A group{{ group.pk }} -j {{ rulset.default_action }}
{% endif %}
