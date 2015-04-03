"""Create user account 

python create_user.py <username> <uid>

If <uid> > 5000 then user is guest.
Other user is considered aifdr staff (1000 < uid < 2000)

See /etc/passwd for available uids

All new users will have primary group 'modelling' and secondary group aifdr or guest based on uid
"""

import os, sys

def usage():
    print 'Usage:'
    print 'sudo python create_user.py <username> <uid>'

def run(s):
    print s
    os.system(s)
    
if __name__ == '__main__':
    
    N = len(sys.argv)
    
    if not N == 3:
        usage()
        sys.exit()
        
    username = sys.argv[1]
    try:
        uid = int(sys.argv[2])
    except:
        msg = 'Could not understand uid'
        print msg
        usage()
        import sys; sys.exit()

    if uid > 5000:
        secondary_group = 'guest'
    else:
        secondary_group = 'aifdr'
                
    run('adduser %s --uid %i' % (username, uid))
    run('usermod --gid modelling %s' % username)
    run('usermod -a --groups modelling %s' % username)    
    run('usermod -a --groups %s %s' % (secondary_group, username))        
    
    

    
