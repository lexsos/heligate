#!/bin/sh

../manage.py accounts_clear_entries
../manage.py events_clear
../manage.py reg_static_ip
../manage.py firewall_gen_config | /bin/sh
../manage.py squid3_intercept_conf | /bin/sh
../manage.py squid3_update_users | /bin/sh
