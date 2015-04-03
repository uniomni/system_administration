"""Restart relevant daemons on server. 
It appears to be cleaner to stop all and then start all rather than calling restart on each service.
"""
import os


# Use restart for networking lest connection is lost
for daemon in ['networking']:
    cmd = '/etc/init.d/%s restart' % daemon
    print cmd
    os.system(cmd)


# Other services
services = ['isc-dhcp-server',
            'nfs-kernel-server',
            'idmapd',
            'tftpd-hpa',
            'bind9',
            'ntp']

print
print '-----------------'
print 'Stop all services'
print '-----------------'
for daemon in services:

    #if daemon in ['tftpd-hpa']:
    #else:
    #    # Service stop does not work for all 
    #    # http://serverfault.com/questions/291992/confusion-on-networking-service-start-stop-in-ubuntu
    cmd = 'service %s stop' % daemon
    print cmd
    os.system(cmd)

print
print '------------------'
print 'Start all services'
print '------------------'
for daemon in services:
    #cmd = '/etc/init.d/%s start' % daemon
    cmd = 'service %s start' % daemon
    print cmd
    os.system(cmd)


