#!/bin/bash

modprobe bonding mode=0 miimon=100 # load bonding module

ifconfig eth0 down	# putting down the eth0 interface
ifconfig eth1 down	# putting down the eth1 interface

ifconfig bond0 hw ether 00:11:22:33:44:55 # changing the MAC address of the bond0 interface
ifconfig bond0 192.168.11.10 up	# to set ethX interfaces as slave the bond0 must have an ip.

ifenslave bond0 eth0	# putting the eth0 interface in the slave mod for bond0
ifenslave bond0 eth1	# putting the eth1 interface in the slave mod for bond0


# http://www.linuxhorizon.ro/bonding.html
