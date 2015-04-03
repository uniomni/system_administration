"""Remove user account for Subversion and TRAC

Usage:

python remove_user.py <username>

See also create_user.py for creation of Subversion/TRAC user ids.

This script must be run as root or using sudo.
"""

import os, sys
from utilities import run, header, makedir, open_log, update_authentication_file
from config import password_filename, auth_filename
from config import filenames_updated

def usage():
    print 'Usage:'
    print 'sudo python remove_user.py <username>'

    
def remove_useraccount(username):    
    """Remove user from password file and clean up
    """
    
    fid = open(password_filename)
    lines = fid.readlines()
    fid.close()
    
    found = False
    for line in lines:
        if line.startswith(username):
            found = True
    
    if not found:
        print('WARNING: User %s was not found in %s' % (username, password_filename))
        return

    # Remove user from password file
    fid = open(password_filename, 'w')
    for line in lines:
        fields = line.split(':')
        if fields[0] != username:
            # Write back
            fid.write(line)
    fid.close()
    filenames_updated[password_filename] = 1
    

if __name__ == '__main__':
    
    N = len(sys.argv)
    
    if N != 2:
        usage()
        sys.exit()
        
    username = sys.argv[1]
    remove_useraccount(username)
    
        
    # Remove user from authentication file    
    # TODO
    # remove_user_from_authentication_file(username)
    
    

    
    # Restart web server
    run('/etc/init.d/apache2 restart')    
    
    print 'Files modified:'
    print filenames_updated.keys()
    print 
    print 'Possibly modify file %s for access details' % auth_filename
    #os.system('cat %s' % auth_filename)        
