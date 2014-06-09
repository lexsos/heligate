#!/bin/sh

../manage.py firewall_update_classifier | /bin/sh
../manage.py squid3_update_users | /bin/sh
