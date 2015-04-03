"""Install Ganglia monitor on Ubuntu 9.04 cluster

Head node:
   apache
   gmond
   gmetad
   
Compute nodes 
   gmond
      

This is based on 
  http://debianclusters.cs.uni.edu/index.php/Ganglia:_Installation
  
with a bunch of additional packages that were implied.

Use this script as root or sudo:

python install_ganglia.py

Then check by pointing your browser to

http://localhost/ganglia

Manual steps:
Start daemon /etc/init.d/ganglia-monitor on each node or reboot them.


See also

Cluster Monitoring With Ganglia: http://www.linux-mag.com/id/1433
Marching Penguins: http://www.linux-mag.com/id/6776

"""

from config import nodes_to_build, head_hostname, client_image_dir


import os
os.system('apt-get update')

for package in ['apache2',
                'rrdtool',
                'librrds-perl',
                'librrd2-dev',
                'php5-gd',
                'ganglia-monitor',
                'gmetad',
                'libapr1-dev',
                'libconfuse0',
                'libconfuse-dev',
                'python-dev']:
    os.system('apt-get -y install %s' % package)
    

#-------------------------------------------------
# Download and install tarball of ganglia frontend
#-------------------------------------------------

ganglia = 'ganglia-3.1.2'
tarball = '%s.tar.gz' % ganglia
sfloc = 'http://sourceforge.net/projects/ganglia/files/ganglia%20monitoring%20core/3.1.2%20%28Langley%29/'
if not os.path.isfile(tarball):
    path = sfloc + tarball + '/download'
    cmd = 'wget ' + path
    os.system(cmd)

s = 'tar xvfz %s' % tarball
os.system(s)

s = 'cd %s; ./configure --prefix=/opt/ganglia --enable-gexec --with-gmetad' % ganglia
print s
os.system(s)

s = 'cd %s; make' % ganglia
print s
os.system(s)

s = 'cd %s; make install' % ganglia
print s
os.system(s)

s = 'mkdir /var/www/ganglia 2>/dev/null'
os.system(s)

s = 'cp -R %s/web/* /var/www/ganglia' % ganglia
os.system(s)

s = '/etc/init.d/apache2 restart'
os.system(s)


#-----------------------------
# Configure host (gmetad.conf)
#-----------------------------

# These are nodes to get information from - not all nodes.
source_string = 'data_source alamba 10 localhost '
for node in nodes_to_build[::4]:
    source_string += '%s ' % node

source_string += '\n'    
grid_string = 'gridname "AIFDR"\n'
config_strings = [source_string, grid_string, 'setuid_username ganglia\n']

# Write new config file
fid = open('/etc/gmetad.conf', 'w')
for line in config_strings:
    fid.write(line)
    
fid.close()    


#-----------------------------
# Configure host (gmond.conf)
#-----------------------------
#
name_string = 'name "%s"\n' % head_hostname
owner_string = 'owner "AIFDR"\n'
url_string = 'url "http://www.aifdr.org"\n'
mcast_string = 'mcast_if eth1\n' # Hardwire ethernet card for head node 
num_string = 'num_nodes %i\n' % len(nodes_to_build)
dmax_string = 'host_dmax 3600\n' # Number of seconds before a dead host is removed

config_strings = [name_string, owner_string, url_string, mcast_string, num_string, dmax_string]

# Write new config file
fid = open('/etc/gmond.conf', 'w')
for line in config_strings:
    fid.write(line)
    
fid.close()    


#-----------------------------
# Configure nodes (gmond.conf)
#-----------------------------

# Use same as head node except for ethernet card (hardwired for alamba cluster0
mcast_string = 'mcast_if eth0\n'
config_strings = [name_string, owner_string, url_string, mcast_string, num_string, dmax_string]


for node in nodes_to_build:

    os.chdir(os.path.join(client_image_dir, node, 'etc'))
    fid = open('gmond.conf', 'w')
    for line in config_strings:
        fid.write(line)
    
    fid.close()    
                

#--------
# Restart
#--------

s = '/etc/init.d/gmetad restart'
os.system(s)

s = '/etc/init.d/ganglia-monitor restart'
os.system(s)

print 'Head node daemons started'
print 'You most start the ganglia monitor on each compute node: I.e for node 6'
print 'ssh node6 "sudo /etc/init.d/ganglia-monitor restart"'
print
print 'Alternatively, reboot all compute nodes'
