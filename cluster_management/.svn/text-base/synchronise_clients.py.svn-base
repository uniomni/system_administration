"""Synchronise clients in Beowulf cluster to head node

This script will update clients system files to match head node.


Distribute entire filesystem except /home and those files mention in
the exclude list to a remote host using rsync.
Useful for maintaining a cluster of identically configured machines

Ole Nielsen - SUT 2003/AIFDR 2009
"""

#-------------------------
# List directories to sync
#-------------------------

sync_dirs = ['/usr', '/etc', '/bin', '/lib', '/sbin', '/root', '/var/lib']

#-------------------------------------------
# List items to exclude from synchronisation
#-------------------------------------------

exclude = ['lost+found', '/lib/modules', '/lib/udev', '*~', '.#*']

# These are critical files related to /etc that must not be copied to nodes
exclude += ['/etc/fstab',
            '/etc/exports',
            '/etc/resolv.conf',
            '/etc/crontab',
            '/etc/hostname',
            '/etc/hosts',
            '/etc/mtab',
            '/etc/ntp.conf',
            '/etc/network',
            '/etc/init.d',
            '/etc/adjtime',
            '/etc/cron.d',
            '/etc/udev/rules.d',
            '/etc/apache2',
            '/etc/gmetad.conf',
            '/etc/gmond.conf',
            '/etc/bind',
            '/etc/dhcp',
            '/etc/ld.so.cache',
            'bind9',
            'dhcp-server',
            'isc-dhcp-server',
            'initramfs.conf',
            '/etc/default/ntp',
            '/etc/default/tftpd-hpa',
            'tftpd-hpa.conf',
            'K20isc-dhcp-server',
            'S20isc-dhcp-server',
            'K85bind9',
            'K77ntp',
            'S15bind9',
            'S23ntp',
            '/usr/share/doc',
            '/usr/lib/nx',
            '/etc/nxserver',
            '/etc/nxagent',
            '/usr/share/freenx-server',
            '/var/run/freenx-server']


#----------------------------------------------
# List individual files that should be included
#----------------------------------------------

sync_files = ['/etc/init.d/ntp']

#------------------------
# Start script in earnest
#------------------------
excludelist = ''
for ex in exclude:
    excludelist += '--exclude="%s" ' % ex


# Get list of hostnames in hostfile except own hostname
import sys, os, os.path
from config import nodes_to_build, head_hostname, client_image_dir
import time

print time.asctime()
print 'Distributing from %s to hosts %s:' % (head_hostname, nodes_to_build)

for host in nodes_to_build:
    print ' Synchronising client %s' % host

    for dir in sync_dirs:
        # rsync
        # Recursive (r)
        # Preserve symlinks (l)
        # Preserve hardlinks (H)
        # Preserve permissions (p)
        # Cope files as whole (W)
        # Preserve modification times (t)
        # Verbose (v)

        cmd = 'rsync -rlHpWt %s --exclude=%s %s %s/%s'\
            % (excludelist, client_image_dir, dir, client_image_dir, host)
        #print cmd
        os.system(cmd)


    for file in sync_files:
        cmd = 'rsync -pWt %s %s/%s%s'\
            % (file, client_image_dir, host, file)
        #print cmd
        os.system(cmd)



