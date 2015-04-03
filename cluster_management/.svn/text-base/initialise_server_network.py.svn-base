"""One off initialisation of server network and necessary packages needed to 
build entire cluster
"""

from config import external_nameserver

import os

fid = open('/etc/resolv.conf', 'w')
fid.write('nameserver %s\n' % external_nameserver)
fid.close()

fid = open('/etc/network/interfaces', 'w')
fid.write('''
auto lo
iface lo inet loopback

auto eth7
iface eth7 inet static
 address 192.168.1.10
 netmask 255.255.255.0
 gateway 192.168.1.1
 route add -net 0.0.0.0 netmask 0.0.0.0 gw 192.168.1.1 eth7
''')


os.system('/etc/init.d/networking restart')
os.system('ifup eth7')

for s in ['ping -c 5 192.168.1.1',
 	  'ping -c 5 %s' % external_nameserver,
          'ping -c 5 www.google.co.id']:

    print s
    os.system(s)

print 'If these pings works, you can move onto install_initial_packages.py'


