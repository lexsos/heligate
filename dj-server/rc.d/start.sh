#!/bin/sh

../manage.py accounts_clear_entries
../manage.py reg_static_ip
../manage.py firewall_gen_config | /bin/sh