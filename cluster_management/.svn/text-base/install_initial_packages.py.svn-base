"""Install packages necessary for building the cluster
It is assumed that internet connection has been established e.g. by running initialise_server.py
"""
import os
os.system('apt-get update')

for package in ['nfs-kernel-server',
                'nfs-common',
                'openssh-server',
                'bind9',
                'dhcp3-server',
                'tftpd-hpa',
                'ifenslave',
                'ntp']:
    os.system('apt-get -y install %s' % package)

