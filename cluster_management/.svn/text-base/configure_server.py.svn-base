"""Configure head node (server) in Beowulf cluster

This script will set up the network and pxe configuration

Must be run as root or with sudo
"""

from utilities import get_class_c_addr, reverse_addr
from config import *
import os, string


# Create a backup of the original /etc area before modifying anything.
# If on already exists, don't do it again.
etc_backup = '/etc_original'
if not os.path.exists(etc_backup):
    s = 'rsync -az /etc %s' % etc_backup
    print s
    os.system(s)



print 'Creating dhcp configuration file'
# Create DHCP configuration file on server
# The IP address listed under fixed-address is the one
# used by PXE at boot time.
os.chdir('/etc/dhcp')  # Changed from dhcp3 to dhcp in Ubuntu 11.04

fid = open('dhcpd.conf', 'w')
fid.write('''
ddns-update-style none;
default-lease-time 600;
max-lease-time 7200;
authoritative;
log-facility local7;
allow booting;
allow bootp;''')
fid.write('\n\n')

class_c_addr = get_class_c_addr(head_ip)
subnet_addr = class_c_addr + '.0'
lower_range_addr = class_c_addr + '.10'
upper_range_addr = class_c_addr + '.50'
broadcast_addr = class_c_addr + '.255'

subnet_statement = 'subnet %s netmask %s {\n' % (subnet_addr,
                                                 netmask)
subnet_statement += '       range %s %s;\n' % (lower_range_addr,
                                               upper_range_addr)
subnet_statement += '       option broadcast-address %s;\n' % broadcast_addr
subnet_statement += '}'

fid.write(subnet_statement)
fid.write('\n\n\n')

for hostname in nodes:

    # First do block for PXE card
    host_statement = 'host %s_%s {\n' % (hostname, '_pxe')

    mac = nodes[hostname].pxe.mac
    macaddr_with_colons = string.join(mac.split('-'), ':')

    host_statement += '    hardware ethernet %s;\n' % macaddr_with_colons
    host_statement += '    fixed-address %s;\n' % nodes[hostname].pxe.ip

    host_statement += '    filename "/pxelinux.0";\n'
    host_statement += '}'

    fid.write(host_statement)
    fid.write('\n\n')


    # NOTE: This was taken out on 23th September 2011 by Rangga and Ole, due to ongoing confusions regarding NIC mappings on the cluster. See ticket:9 - http://www.aifdr.org/projects/system_administration/ticket/9
    # Now do block for network connection

    #host_statement = 'host %s {\n' % hostname

    #mac = nodes[hostname].net.mac
    #macaddr_with_colons = string.join(mac.split('-'), ':')

    #host_statement += '    hardware ethernet %s;\n' % macaddr_with_colons
    #host_statement += '    fixed-address %s;\n' % nodes[hostname].net.ip
    #host_statement += '}'

    #fid.write(host_statement)
    #fid.write('\n\n')


fid.close()



# Configure TFTPD
# Create tftpd server configuration file
print 'Creating tftpd-hpa file'
os.chdir('/etc/default')
fid = open('tftpd-hpa', 'w')
fid.write(auto_generate_disclaimer)
fid.write('TFTP_USERNAME="tftp"\n')
fid.write('TFTP_DIRECTORY="/var/lib/tftpboot"\n')
fid.write('TFTP_ADDRESS="0.0.0.0:69"\n')
fid.write('TFTP_OPTIONS="--secure"\n')
#fid.write('RUN_DAEMON="yes"\n')
#fid.write('OPTIONS="-l -s /var/lib/tftpboot"\n')
fid.close()


# Create setting to ensure correct NFS4 user id mapping.
# The service envoking this idmapd and not nfs-common
# The file will be sync'd to the compute nodes who also need it
print 'Creating nfs-common file'
os.chdir('/etc/default')
fid = open('nfs-common', 'w')
fid.write(auto_generate_disclaimer)
fid.write('RPCNFSDCOUNT=8\n')
fid.write('RPCNFSDPRIORITY=0\n')
fid.write('RPCMOUNTDOPTS=--manage-gids\n')
fid.write('NEED_SVCGSSD=\n')
fid.write('RPCSVCGSSDOPTS=\n')
fid.write('NEED_STATD=yes\n')  # FIXME: I don't think that solved the problem. Try to remove again
fid.write('STATDOPTS=\n')
fid.write('NEED_IDMAPD=yes\n')
fid.write('NEED_GSSD=\n')
fid.close()

# Ensure idmapd starts at boot time. This is following fix posted here:
#https://bugs.launchpad.net/ubuntu/+source/mountall/+bug/643289/comments/10
# The file will be sync'd to the compute nodes who also need it
os.chdir('/etc/init')
fid = open('idmapd.conf')
lines = fid.readlines()
fid.close()

fid = open('idmapd.conf', 'w')
for line in lines:
    # Store all lines except those starting with umask
    if line.strip().startswith('start on (local-filesystems'):
        fid.write('# Suggestion from https://bugs.launchpad.net/ubuntu/+source/mountall/+bug/643289/comments/10\n')
        fid.write('start on (net-device-up or mounting TYPE=nfs4)\n')
    else:
        fid.write(line)

fid.close()


print 'Creating exports file'
# Create exports file with all clients
os.chdir('/etc')

fid = open('exports', 'w')
for hostname in nodes:
    client_dir = os.path.join(client_image_dir, hostname)

    ip_info = '%s/255.255.255.255' % nodes[hostname].pxe.ip
    fid.write('%s %s(%s)\n' % (client_dir, ip_info, nfs_permissions))

    # NOTE: This was taken out on 23th September 2011 by Rangga and Ole, due to ongoing confusions regarding NIC mappings on the cluster. See ticket:9 - http://www.aifdr.org/projects/system_administration/ticket/9
    # FIXME - uncomment!!!!
    ip_info = '%s/255.255.255.255' % nodes[hostname].net.ip
    fid.write('%s %s(%s)\n' % (client_dir, ip_info, nfs_permissions))

# Allow all compute nodes to nfs mount to shared area
client_dir = os.path.join(client_image_dir, shared_dir)

ip_info = '%s/255.255.255.0' % nodes[hostname].net.ip # Any ip
fid.write('%s %s(%s)\n' % (client_dir, ip_info, nfs_permissions))

fid.close()

# Update head node identity
print 'Updating server identity and network'
os.chdir('/etc')

fid = open('hostname', 'w')
fid.write(head_hostname + '\n')
fid.close()

fid = open('hosts', 'w')
fid.write('127.0.0.1        localhost\n')
fid.write('127.0.1.1        %s\n' % head_hostname)
#fid.write('%s               www.aifdr.org\n' % web_ip)  # FIXME: Why? See file in bind/zones.
fid.close()


# Create modprobe aliases for network bonding
# FIXME: This maybe unnecessary in Ubuntu 10.4 and newer
os.chdir('/etc/modprobe.d')
fid = open('aliases.conf', 'w')
fid.write('alias bond0 bonding\n')
fid.write('options bond0 mode=0 miimon=100 downdelay=200 updelay=200 max_bonds=2\n')
fid.close()


# Set network parameters for head node
os.chdir('/etc/network')
fid = open('interfaces', 'w')
fid.write('''auto lo
iface lo inet loopback

''')

# NOTE: Ethernet cards are hardwired for the alamba cluster
for (interface, ip) in [('eth1', head_ip),
                        ('eth2', head_storage_ip),
                        ('eth4', head_internet_ip),
                        ('eth5', head_management_ip)]:
    gateway = get_class_c_addr(ip) + '.1'
    fid.write('auto %s\n' % interface)
    fid.write('iface %s inet static\n' % interface)
    fid.write(' address %s\n' % ip)
    fid.write(' netmask %s\n' % netmask)
    if interface == 'eth4':
        # Needs gateway for internet connection.
        fid.write(' gateway %s\n' % gateway)
    fid.write('\n')

# Bonding section of interfaces (storage net)
# FIXME (Ole): Network cards are hardwired
#
# NO LONGER NEEDED: See https://help.ubuntu.com/community/UbuntuBonding
#
#for eth in ['eth2', 'eth3']:
#    fid.write('auto %s\n' % eth)
#    fid.write('iface %s inet manual\n\n' % eth)

#fid.write('auto bond0\n')
#fid.write('iface bond0 inet static\n')
#fid.write('        address %s\n' % head_storage_ip)
#fid.write('        netmask %s\n' % netmask)
#fid.write('        bond-slaves eth2 eth3\n')
##fid.write('        up /sbin/ifenslave bond0 eth2 eth3\n')
##fid.write('        pre-down /sbin/ifenslave -d bond0 eth2 eth3\n')
#fid.close()

# Allow symbolic node names to be used without full domain.
os.chdir('/etc')
fid = open('resolv.conf', 'w')
fid.write('domain %s\n' % domain_name)
fid.write('search %s\n' % domain_name)
fid.write('nameserver %s\n' % head_ip)
fid.write('nameserver %s\n' % external_nameserver)
fid.close()

# Remove network manager, so that it doesn't overwrite network settings
cmd = 'apt-get -q -y purge network-manager network-manager-gnome'
print cmd
os.system(cmd)

# Manually force mount of all
os.chdir('/etc')
fid = open('rc.local', 'w')
fid.write('#!/bin/sh -e\n\n')
fid.write(auto_generate_disclaimer)
fid.write('mount -a\n')
fid.write('exit 0\n')
fid.close()

# Configure server's mount table (fstab)
os.chdir('/etc')
fid = open('fstab','w')
# FIXME (Ole): This is the local filesystems hardwired

fid.write("""
# /etc/fstab: static file system information.
#
# Use 'blkid -o value -s UUID' to print the universally unique identifier
# for a device; this may be used with UUID= as a more robust way to name
# devices that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
proc            /proc           proc    nodev,noexec,nosuid 0       0
# / was on /dev/sda1 during installation
UUID=23629062-fc07-4a8c-9ff9-b8843f098088 /               ext4    errors=remount-ro 0       1
# swap was on /dev/sda5 during installation
UUID=900f93bb-1343-4237-abd2-5e6ec1fb90d5 none            swap    sw              0       0

""")

# Now add NFS mount of the NAS - note use version 3 for the NAS, other nobody, nogroup is mapped
for nas_dir in nas_filesystems:
    nas_mount_point = nas_filesystems[nas_dir]
    fid.write('%s /%s nfs defaults,intr,nfsvers=3 1 1\n' % (nas_dir,
                                                            nas_mount_point))
fid.close()

# Create mount points for NAS filesystems at the root level
for nas_dir in nas_filesystems:
    nas_mount_point = nas_filesystems[nas_dir]
    os.system('mkdir /%s 2>/dev/null' % nas_mount_point)



print 'Configuring DNS server'
try:
    os.mkdir('/etc/bind/zones')
except:
    pass

os.chdir('/etc/bind/zones')

fid = open('%s.db' % domain_name, 'w')
x = (domain_name,)*3 + (head_ip,)*2
s = '''
;
; BIND data file for local interface
;
$TTL	604800
@	IN	SOA	%s. root.%s. (
			      2		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	ns.%s.
@	IN	A	%s
@	IN	AAAA	::1
ns      IN      A       %s
''' % x
fid.write(s)

for hostname in nodes:
    # NOTE: This was changed from .net.ip on 23th September 2011 by Rangga and Ole, due to ongoing confusions
    # regarding NIC mappings on the cluster. See ticket:9 - http://www.aifdr.org/projects/system_administration/ticket/9
    fid.write('%s\tIN\tA\t%s\n' % (hostname,
                                   nodes[hostname].pxe.ip))

# FIXME: Nas Servers hardwired for now
fid.write('''
nas-server-1	A	192.168.20.11
nas-server-2	A	192.168.20.12
''')

# Allow name resolution of things like www.aifdr.org (but this didn't seem to work, so we put it in hosts)
fid.write('www\tIN\tA\t%s\n'  % web_ip)
fid.close()


# Create bind configuration
class_c_addr = get_class_c_addr(head_ip)
reverse_class_c_addr = reverse_addr(class_c_addr)

os.chdir('/etc/bind')

fid = open('named.conf.local', 'w')
name_twice = (domain_name,)*2
fid.write('''
zone "%s" {
	type master;
	file "/etc/bind/zones/%s.db";
};
''' % name_twice)

fid = open('named.conf.options', 'w')
name_twice = (domain_name,)*2
ip_twice = (reverse_class_c_addr,)*2
fid.write('''
options {
        directory "/var/cache/bind";

        // Forward to external nameserver
        forwarders {
                %s;
        };

        auth-nxdomain no;    # conform to RFC1035
        listen-on-v6 { any; };
};
''' % external_nameserver)


print 'Configuring /etc/profile'
# Add umask 0002 to /etc/profile (if not already there) to ensure groups get write access to new files
# rw-rw-r--
fid = open('/etc/profile')
lines = fid.readlines()
fid.close()

fid = open('/etc/profile', 'w')
for line in lines:
    # Store all lines except those starting with umask
    if not line.strip().startswith('umask'):
        fid.write(line)

# Add umask so that group gets write access by default
fid.write('umask 0002\n')
fid.close()

print 'Adding node synchronisation to crontab if needed'
# Update system crontab with synchronisation of nodes
fid = open('/etc/crontab')
lines = fid.readlines()
fid.close()

keep = True
fid = open('/etc/crontab', 'w')
for line in lines:

    # First get rid of any old cluster_management entry
    if line.startswith('# Synchronise'):
        keep = False

    # A blank line signifies that we are done with a block
    if line.strip() == '':
        keep = True

    if keep:
        fid.write(line)

# Now add synchronisation information
fid.write('# Synchronise all nodes\n')
fid.write('2 2 * * * root python /etc/system_administration/cluster_management/synchronise_clients.py > /var/log/synchronise_clients.log\n')
fid.close()

print 'Configuring NTP'
# Set up NTP server
fid = open('/etc/ntp.conf', 'w')
fid.write(auto_generate_disclaimer)
fid.write("""
# /etc/ntp.conf, configuration for ntpd; see ntp.conf(5) for help

driftfile /var/lib/ntp/ntp.drift

# Enable this if you want statistics to be logged.
statsdir /var/log/ntpstats/

statistics loopstats peerstats clockstats
filegen loopstats file loopstats type day enable
filegen peerstats file peerstats type day enable
filegen clockstats file clockstats type day enable

# By default, exchange time with everybody, but don't allow configuration.
restrict -4 default kod notrap nomodify nopeer noquery
restrict -6 default kod notrap nomodify nopeer noquery

# Local users may interrogate the ntp server more closely.
restrict 127.0.0.1
restrict ::1

# If you want to provide time to your local subnet, change the next line.
# (Again, the address is an example only.)
broadcast %s

server id.pool.ntp.org
server pool.ntp.org
server nets.org.sg
server ntp.cs.mu.oz.au
""" % broadcast_addr)
fid.close()


# Install missing file to avoid dhcp error in 11.04
# See http://scratching.psybermonkey.net/2011/01/bind-error-loading-from-master-file.html
cmd = 'touch /var/cache/bind/managed-keys.bind'
print cmd
os.system(cmd)

#print 'Checking out fresh copy of cluster_management'
# Check out fresh version of system_administration to /etc
os.chdir('/etc')
os.system('svn co http://www.aifdr.org/svn/system_administration')


