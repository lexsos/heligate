#!/bin/sh

../manage.py accounts_clear_entries
../manage.py message_bus_clear
../manage.py accounts_web_clear_url
../manage.py reg_static_ip
../manage.py firewall_gen_config | /bin/sh
../manage.py squid3_intercept_conf | /bin/sh
../manage.py squid3_update_users | /bin/sh
