"""Configure clients in Beowulf cluster

This script will setup client node
configurations on server
"""

from utilities import get_kernel_name
from config import *
import os, string


kernel_name = get_kernel_name()

print 'Copying network boot system'
# Create PXE config dir
try:
    os.mkdir(pxeconfig_dir)
except OSError:
    pass

# Copy across bootfile
try:
    os.system('cp /usr/lib/syslinux/pxelinux.0 /var/lib/tftpboot')
except OSError:
    pass

# Copy kernel across
try:
    os.system('cp /boot/%s /var/lib/tftpboot' % kernel_name)
except OSError:
    pass


# Generate initramfs.conf (BOOT=nfs is the important bit here)
print 'Generating RAM filesystem image'
fid = open('/etc/initramfs-tools/initramfs.conf', 'w')
fid.write('''
MODULES=most
BUSYBOX=y
COMPCACHE_SIZE=""
COMPRESS=gzip
BOOT=nfs
DEVICE=eth0
NFSROOT=auto''')
fid.close()

# Create RAM filesystem
kernel_version = string.join(kernel_name.split('-')[1:], '-')
os.system('mkinitramfs -o /var/lib/tftpboot/initrd.img-%s' % kernel_version)

print 'Creating configuration files in %s' % pxeconfig_dir
for hostname in nodes:

    # Create configuration files in tftpboot/pxelinux

    config_file = '01-' + nodes[hostname].pxe.mac
    os.chdir(pxeconfig_dir)

    fid = open(config_file, 'w')
    fid.write('LABEL linux\n')
    root_expression = 'root=/dev/nfs'
    initrd_expression = 'initrd=initrd.img-%s' % kernel_version
    nfsroot_expression = 'nfsroot=%s:%s/%s' % (head_ip,
                                               client_image_dir,
                                               hostname)

    line = 'DEFAULT %s %s %s %s ip=dhcp rw' %(kernel_name,
                                              root_expression,
                                              initrd_expression,
                                              nfsroot_expression)
    fid.write(line + '\n')
    fid.close()


# Change permissions for tftpboot. FIXME: is this necessary?
os.system('chmod -R 777 /var/lib/tftpboot')


# Create client image dirs from where they will get their entire system
print 'Creating client image dirs in %s' % client_image_dir

if not os.path.exists(client_image_dir):
    err = 'Client area does not exist. Please run build_clients.py'
    raise Exception(err)

print 'Setting up network for each client'
for hostname in nodes_to_build:
    print 'Configuring client %s' % hostname
    os.chdir(client_image_dir)

    if not os.path.exists(hostname):
        err = 'Client area for host %s does not exist.' % hostname
        err += 'Please run build_clients.py'
        raise Exception(err)

    # Create mount point for shared directories
    os.system('cd %s; mkdir shared 2>/dev/null' % hostname)
    for nas_dir in nas_filesystems:
        nas_mount_point = nas_filesystems[nas_dir]
        os.system('cd %s; mkdir %s 2>/dev/null' % (hostname, nas_mount_point))



    os.chdir(hostname)

    # Replace some by soft links on client
    s = '/bin/rm -rf home; ln -s /%s/home home' % shared_dir
    os.system(s)


    # Change to client's etc area
    os.chdir(os.path.join(client_image_dir, hostname, 'etc'))

    # Create fstab in client area
    fid = open('fstab', 'w')
    fid.write('proc     /proc    proc    defaults       0       0\n')
    fid.write('/dev/nfs	/	 nfs	 defaults	1	1\n')
    fid.write('%s:%s/%s /%s nfs defaults 1 1\n' % (head_ip,
                                                   client_image_dir,
                                                   shared_dir,
                                                   shared_dir))
    for nas_dir in nas_filesystems:
        nas_mount_point = nas_filesystems[nas_dir]
        fid.write('%s /%s nfs defaults,nfsvers=3 1 1\n' % (nas_dir,
                                                           nas_mount_point))
    fid.close()


    # Create hostname file
    fid = open('hostname', 'w')
    fid.write(hostname + '\n')
    fid.close()


    # Create hosts file
    fid = open('hosts', 'w')
    fid.write('127.0.0.1        localhost\n')
    fid.write('127.0.1.1        %s\n' % hostname)
    fid.close()

    # Create persistent names for network interfaces (I don't believe this works - the static allocation in /etc/network/interfaces is the way to go, so I am sure this bit could be deleted. No harm though.)
    os.chdir(os.path.join(client_image_dir, hostname, 'etc/udev/rules.d'))
    fid = open('70-persistent-net.rules', 'w')
    interfaces = mac_addr[hostname]
    for eth in interface_names:
        mac = interfaces[eth]
        macaddr_with_colons = string.join(mac.split('-'), ':')

        fid.write('# Ethernet device %s\n' % eth)
        fid.write('SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="%s", ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="eth*", NAME="%s"\n\n' % (macaddr_with_colons, eth))

    # FIXME: Temp cleanup
    #os.system('/bin/rm -rf %s/%s/etc/udev/rules.d/70-persistent-net.rules' % (client_image_dir, hostname))


    # Create modprobe aliases for network bonding (FIXME: All the bonding stuff could be deleted)
    os.chdir(os.path.join(client_image_dir, hostname, 'etc/modprobe.d'))
    fid = open('aliases.conf', 'w')
    fid.write('alias bond0 bonding\n')
    fid.write('options bond0 mode=0 miimon=100 downdelay=200 updelay=200 max_bonds=2\n')
    fid.close()

    # Create network interfaces file (with static address)
    os.chdir(os.path.join(client_image_dir, hostname, 'etc/network'))
    fid = open('interfaces', 'w')
    #fid.write('auto lo %s %s %s %s\n' % tuple(interface_names))
    fid.write('auto lo\n')
    fid.write('iface lo inet loopback\n\n')

    fid.write('auto eth0\n')
    fid.write('iface eth0 inet static\n')
    fid.write('        address %s\n' % nodes[hostname].pxe.ip)
    fid.write('        netmask %s\n' % netmask)
    fid.write('        gateway 192.168.11.1\n\n')  # FIXME Derive

    fid.write('auto eth1\n')
    fid.write('iface eth1 inet static\n')
    fid.write('        address %s\n' % nodes[hostname].nas.ip)
    fid.write('        netmask %s\n' % netmask)


    # Bonding section of interfaces (storage net)
    # FIXME (Ole): Network cards are hardwired
    #for eth in ['eth5', 'eth6']:
    #    fid.write('iface %s inet dhcp\n\n' % eth)

    #fid.write('auto bond0\n')
    #fid.write('iface bond0 inet static\n')
    #fid.write('        address %s\n' % nodes[hostname].nas.ip)
    #fid.write('        netmask %s\n' % netmask)
    #fid.write('        post-up /sbin/ifenslave bond0 eth7 eth8\n')
    #fid.close()

    # Set DNS server to head node in all compute nodes
    os.chdir(os.path.join(client_image_dir, hostname, 'etc'))
    fid = open('resolv.conf', 'w')
    fid.write('search %s\n' % domain_name)
    fid.write('nameserver %s\n' % head_ip)
    fid.close()

    # Manually force mount of all
    # This is now sync'd from the head node
    #os.chdir(os.path.join(client_image_dir, hostname, 'etc'))
    #fid = open('rc.local', 'w')
    #fid.write(auto_generate_disclaimer)
    #fid.write('mount -a\n')
    #fid.write('exit 0\n')
    #fid.close()


    # Add umask 0002 to /etc/profile (if not already there) to ensure groups get write access to new files
    # rw-rw-r--
    os.chdir(os.path.join(client_image_dir, hostname, 'etc'))
    fid = open('profile')
    lines = fid.readlines()
    fid.close()

    fid = open('profile', 'w')
    for line in lines:
        # Store all lines except those starting with umask
        if not line.strip().startswith('umask'):
            fid.write(line)

    # Add umask
    fid.write('umask 0002\n')
    fid.close()


    # Configure NTP to use head node for time synchronisation
    os.chdir(os.path.join(client_image_dir, hostname, 'etc'))
    fid = open('ntp.conf', 'w')
    fid.write(auto_generate_disclaimer)
    fid.write('driftfile /var/lib/ntp/ntp.drift\n')
    fid.write('server %s\n' % head_ip)
    fid.close()

    # Enable X11 forwarding on each node (write new sshd_config)
    os.chdir(os.path.join(client_image_dir, hostname, 'etc', 'ssh'))
    fid = open('sshd_config', 'w')
    fid.write("""
Port 22
Protocol 2

HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_dsa_key

UsePrivilegeSeparation yes

KeyRegenerationInterval 3600
ServerKeyBits 768

SyslogFacility AUTH
LogLevel INFO

LoginGraceTime 60
PermitRootLogin no
StrictModes yes

RSAAuthentication yes
PubkeyAuthentication yes

IgnoreRhosts yes
RhostsRSAAuthentication no
HostbasedAuthentication no

PermitEmptyPasswords no

ChallengeResponseAuthentication no

X11Forwarding yes
X11DisplayOffset 10
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes

AcceptEnv LANG LC_*

Subsystem sftp /usr/lib/openssh/sftp-server

UsePAM yes

ClientAliveInterval 15
ClientAliveCountMax 5
""")
    fid.close()
