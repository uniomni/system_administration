"""Remove Subversion and TRAC project
Update configuration files accordingly
"""
from config import password_filename, auth_filename, trac_home, svn_home
from utilities import run, consolidate_configuration_files
import os, sys

def usage():
    print 'Usage:'
    print 'sudo python remove_project.py <project>'


if __name__ == '__main__':
    N = len(sys.argv)
    if N != 2:
        usage()
        sys.exit()
        
    project = sys.argv[1]
        
    print 'WARNING: This will remove Subversion repository and TRAC pages for project %s' % project
    answer = raw_input('Continue? (Y/N) [N]')
    if answer.upper() != 'Y':
        print 'Nothing done'
        sys.exit()

    answer = raw_input('Are you sure? (Y/N) [N]')
    if answer.upper() != 'Y':
        print 'Nothing done'
        sys.exit()

    for dir in [trac_home, svn_home]:
        s = '/bin/rm -rf %s' % os.path.join(dir, project)
        run(s)

    # Cleanup configuration files
    consolidate_configuration_files()
    
    # Restart web server
    run('/etc/init.d/apache2 restart')

