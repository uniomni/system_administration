"""Install the CMS Joomla on Ubuntu
"""

import os
os.system('apt-get update')

for package in ['apache2',
                'php5-mysql',
                'mysql-client',
                'mysql-server',
                'libapache2-mod-auth-mysql']:
                
    s = 'apt-get -y install %s' % package
    print(s)
    os.system(s)
    

    
#---------------------------------------
# Download and install tarball of joomla
#---------------------------------------


joomla = 'Joomla_1.5.15-Stable-Full_Package'
tarball = '%s.tar.gz' % joomla
location = 'http://joomlacode.org/gf/download/frsrelease/11396/45609/'
if not os.path.isfile(tarball):
    path = location + tarball
    cmd = 'wget ' + path
    os.system(cmd)

s = 'mkdir /var/www/joomla; cp %s /var/www/joomla; cd /var/www/joomla; tar xvfz %s' % (tarball, tarball)
print(s)
os.system(s)
    
s = 'chown -R www-data:www-data /var/www/joomla'
print(s)
os.system(s)    
    

# Set Joomla database in MySQL
s = 'mysqladmin -f -p drop Joomla'
print(s); os.system(s)

s = 'mysqladmin -p create Joomla'
print(s); os.system(s)

# Perhaps restart mysql and apache
os.system('/etc/init.d/mysql restart')
os.system('/etc/init.d/apache2 restart')



# MySQL will prompt for the database admin password and then create
# the initial database files.  Next you must manually login and set the access
# database rights e.g.
#
#$ mysql -p
#
# and then 
#
#CREATE USER joomla@www.aifdr.org IDENTIFIED BY 'dstat43';
#GRANT ALL PRIVILEGES ON Joomla.* TO joomla@www.aifdr.org IDENTIFIED BY 'dstat43';
#
#to activate the new permissions you must enter the command
#flush privileges;
#and then enter '\q' to exit MySQL.
#
# Then point web browser to
# 
#http://localhost/joomla
#
#and follow instructions
#
# Use localhost when asked about mysql connection
#
#
#
#
# After going through the web installation, delete subdir /var/www/html/installation
# Then login with username: admin and password as above.

# Needed to update postfix:
#wajig reinstall postfix
#Setting up postfix (2.5.5-1.1) ...
#
#Postfix was not set up.  Start with 
#  cp /usr/share/postfix/main.cf.debian /etc/postfix/main.cf
#  .  If you need to make changes, edit
#  /etc/postfix/main.cf (and others) as needed.  To view Postfix configuration
#  values, see postconf(1).
#  
#  After modifying main.cf, be sure to run '/etc/init.d/postfix reload'.
# 
# I did
#/etc/init.d/postfix restart
# /etc/init.d/postfix reload
  
  
  
  
# BACKUP and RESTORE
# 
# Use Akeeba http://www.akeebabackup.com/
#
# Backup using akeeba module
# Then mv kickstart.php and module to /var/www/<newarea>
# Change permissions: chown -R www-data:www-data /var/www/<newarea>
# Point web browser to www.aifdr.org/<newarea>/kickstart.php and follow instructions. Normally nothing should have to change.







