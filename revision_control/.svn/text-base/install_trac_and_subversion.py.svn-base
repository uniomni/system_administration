from utilities import run

def install_packages():    
    """Get required Ubuntu/Debian packages.
       It is OK if they are already installed
    """
       
    for package in ['apache2',
                    'subversion',
                    'trac',    
                    'libapache2-svn',
                    'libapache2-mod-python', 
                    'libapache2-mod-python-doc']:

        if package == 'trac':
            # Hack to get TRAC 0.11.4 on Ubuntu <9.04
            # See http://serverfault.com/questions/11851/attachments-not-showing-up-in-trac

            s = 'apt-get remove trac'
            run(s)
            s = 'easy_install http://svn.edgewall.org/repos/trac/tags/trac-0.11.4'
            run(s)
            continue
        
        s = 'apt-get -y install %s > %s_install.log' % (package, package)
        err = run(s)
        if err != 0:
            msg = 'Installation of package %s failed. ' % package
            msg += 'See log file %s_install.log for details' % package
            raise Exception(msg)
    
if __name__ == '__main__':
    install_packages()
