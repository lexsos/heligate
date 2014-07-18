#!/bin/sh

#stop squid
/etc/init.d/squid3 stop

# stop forwarding
echo 0 > /proc/sys/net/ipv4/ip_forward

# clear iptables rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
