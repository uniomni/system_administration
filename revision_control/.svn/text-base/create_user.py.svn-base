"""Create or modify user account for Subversion and TRAC

Usage:

python create_user.py <username> [<encrypted password>]

If user already exists, password will be modified.

See also create_project.py for creation of Subversion/TRAC user ids.

This script must be run as root or using sudo.
"""

import os, sys
from utilities import run, header, makedir, open_log, update_authentication_file
from config import password_filename, auth_filename
from config import filenames_updated

def usage():
    print 'Usage:'
    print 'sudo python create_user.py <username> [<encrypted password>]'


def create_useraccount_interactively(username):

    if os.path.isfile(password_filename):
        cmd = 'htpasswd -m'
    else:
        cmd = 'htpasswd -cm'        
        
    s = cmd + ' %s %s' % (password_filename, username)    
    run(s)
    filenames_updated[password_filename] = 1

    
def create_useraccount_from_encrypted_password(username, password):    
    """Create account for user with supplied encrypted password
    
    The password file (typically dav_svn.passwd) is modified.
    If user already exists, the supplied encrypted password will replace the existing password
    If user does not exist a new entry with username:encrypted_password will be created
    """
    
    fid = open(password_filename)
    lines = fid.readlines()
    fid.close()
    
    found = False
    fid = open(password_filename, 'w')
    for line in lines:
        fields = line.split(':')
        if fields[0] == username:
            fid.write('%s:%s\n' % (username, password))
            found = True
        else:
            fid.write(line)
    
    if not found:
        fid.write('%s:%s\n' % (username, password))
    
    fid.close()
    filenames_updated[password_filename] = 1
    
if __name__ == '__main__':
    
    N = len(sys.argv)
    
    if not 2 <= N <= 3:
        usage()
        sys.exit()
        
    username = sys.argv[1]
    if N == 3:
        create_useraccount_from_encrypted_password(username, sys.argv[2])
    else:    
        create_useraccount_interactively(username)

    update_authentication_file(username)
    
    # Restart web server
    run('/etc/init.d/apache2 restart')    
    
    print 'Files modified:'
    print filenames_updated.keys()
    print 
    print 'Possibly modify file %s for access details' % auth_filename
    #os.system('cat %s' % auth_filename)        
