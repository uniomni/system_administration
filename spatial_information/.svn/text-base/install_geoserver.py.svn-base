"""Install new Geoserver system wide

Usage:

sudo python install_geoserver.py
"""

# Manual steps (v 2.0.1)
# Get rest plugin from 
#http://sourceforge.net/projects/geoserver/files/GeoServer%20Extensions/2.0.1/geoserver-2.0.1-restconfig-plugin.zip/download

# Rest command that worked
#curl -H 'Content-Type: application/zip' 'http://admin:geoserver@www.aifdr.org:8080/geoserver/rest/workspaces/test/coveragestores/Pk50095/file.worldimage' -T Pk50095.zip -X PUT -v

import os
from config import geoserver, update_marker, java_home, geoserver_url, geoserver_rest_plugin, geoserver_rest_plugin_url
from utilities import run, makedir, header, replace_string_in_file, get_shell, set_bash_variable


def install_ubuntu_packages():    
    """Get required Ubuntu packages for geoserver.
       It is OK if they are already installed
    """

    header('Installing Ubuntu packages')     
    
    s = 'apt-get clean'
    run(s, verbose=True)
    
    #s = 'apt-get update'
    #run(s, verbose=True) 

    for package in ['apache2', 'openjdk-6-jre-lib']:

                    
        s = 'apt-get -y install %s' % package
        
        log_base = '%s_install' % package
        try:
            run(s,
                stdout=log_base + '.out',
                stderr=log_base + '.err',                  
                verbose=True)
        except:
            msg = 'Installation of package %s failed. ' % package
            msg += 'See log file %s.out and %s.err for details' % (log_base, log_base)
            raise Exception(msg)
            



def download_and_unpack():    
    """Download geoserver OS independent files
    """

    archive = geoserver + '-bin.zip'


    path = os.path.join(geoserver_url, archive)

    if not os.path.isfile(archive): 
        # FIXME: Should also check integrity of zip file.
        cmd = 'wget ' + path
        run(cmd, verbose=True)


    # Clean out
    s = '/bin/rm -rf /usr/local/%s' % geoserver
    run(s, verbose=True)

    # Unpack
    s = 'unzip %s -d /usr/local' % archive
    run(s, verbose=True)    

def get_plugins():
    """Get plugins such as REST
    """
    
    path = geoserver_rest_plugin_url
    
    if not os.path.isfile(geoserver_rest_plugin): 
        # FIXME: Should also check integrity of zip file.
        cmd = 'wget ' + path
        run(cmd, verbose=True)
    
    # Unpack into geoserver installation
    s = 'unzip %s -d /usr/local/%s/webapps/geoserver/WEB-INF/lib' % (geoserver_rest_plugin, geoserver)
    run(s, verbose=True)        

    

def set_environment():
    """Set up /etc/default/geoserver
    """

    fid = open('/etc/default/geoserver', 'wb')
    
    fid.write('USER=geoserver\n')
    fid.write('GEOSERVER_DATA_DIR=/usr/local/%s/data_dir\n' % geoserver)    
    fid.write('GEOSERVER_HOME=/usr/local/%s\n' % geoserver)
    fid.write('JAVA_HOME=%s\n' % java_home)
    fid.write('JAVA_OPTS="-Xms128m -Xmx512m"\n')

    #GEOSERVER_DATA_DIR=/home/$USER/data_dir
    #GEOSERVER_HOME=/home/$USER/geoserver
    
    fid.close()

def get_daemon():
    """Download geoserver daemon and install into /etc/init.d
    """
    
    # FIXME: Didn't seem to work.
    
    cmd = 'wget http://docs.geoserver.org/stable/en/user/_downloads/geoserver_deb'
    run(cmd, verbose=True)
    
    cmd = 'mv geoserver_deb /etc/init.d/geoserver'
    run(cmd, verbose=True)
    
    cmd = 'chmod +x /etc/init.d/geoserver'
    run(cmd, verbose=True)    
        
def run_startup():
    """Run geoserver startup script
    """

    #cmd = '/etc/init.d/geoserver start'
    #run(cmd, verbose=True)
    
    geo_home = '/usr/local/%s' % geoserver
    cmd = 'export JAVA_HOME=%s; export GEOSERVER_HOME=%s; $GEOSERVER_HOME/bin/startup.sh &' % (java_home, 
                                                                                               geo_home)
    run(cmd, verbose=True)    
    print 'Done'
        
if __name__ == '__main__':

    install_ubuntu_packages()
    download_and_unpack()
    get_plugins()
    set_environment()    
    ##get_daemon()
    run_startup()
