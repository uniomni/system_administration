"""Script to install Ruby on Rails

Usage:

sudo python install_ruby_on_rails.py
"""

import os
#from config import 
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

    for package in ['apache2', 'libxml2', 'libxml2-dev', 'libxslt1-dev', 'postgresql', 'postgis']:
        
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
            

def install_rvm():
    cmd = 'sudo bash < <( curl -L http://bit.ly/rvm-install-system-wide )'
    run(cmd, verbose=True)



def update_profile():
    cmd = 'echo \'[[ -s ""/usr/local/lib/rvm"" ]] && source ""/usr/local/lib/rvm""\' >> ~/.bashrc"'
    run(cmd, verbose=True)    	



# "rvm install 1.8.7
# rvm list
# rvm --default 1.8.7
# ruby -v"		

# gem update --system		

# gem install bundler --pre		


# svn co http://aifdr.org/svn/riat/source/trunk/riat_rails/ --username burqsh		

# "cd ./riat_rails/ 
# bundle install"		


#sudo bash < <( curl -L http://bit.ly/rvm-install-system-wide )
#sudo usermod -a -G rvm nielson
#"rvm install 1.8.7
#rvm list
#rvm --default 1.8.7
#ruby -v"		


if __name__ == '__main__':

    install_ubuntu_packages()
    install_rvm()
    update_profile()
    #download_and_unpack()
    #get_plugins()
    #set_environment()    
    #run_startup()
    
