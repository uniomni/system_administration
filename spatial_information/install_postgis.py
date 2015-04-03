"""This script will install PostGIS
"""

from utilities import run, makedir
from config import postgis
import os


def install_ubuntu_packages():    
    """Get required PostGIS packages.
       It is OK if they are already installed
    """
       
    for package in ['postgresql',
                    'postgresql-server-dev-8.4',
                    'proj',                    
                    'libgeos-dev',
                    'postgis',    # For things like shp2pgsql
                    #'pgadmin3',
                    #'libpq-dev',
                    #'postgresql-contrib',    
                    ]:

        s = 'apt-get -y install %s > %s_install.log' % (package, package)
        run(s)
                  
            
def install_postgis_from_source(postgis):
    makedir(os.path.expanduser('~/Downloads'))                    
                    
    if not os.path.exists('%s.tar.gz' % postgis):
        s = 'wget http://postgis.refractions.net/download/%s.tar.gz' % postgis
        run(s)
    
    s = 'tar xvfz %s.tar.gz' % postgis; run(s)
    
    os.chdir(postgis)
    
    s = './configure'; run(s)
    s = 'make'; run(s)
    s = 'make install'; run(s)                    
                       
if __name__ == '__main__':
    install_ubuntu_packages()
    install_postgis_from_source(postgis)                  

