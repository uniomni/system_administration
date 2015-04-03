"""
"""

import sys
import os
from subprocess import Popen, PIPE

excluded_sites = ['http://www.google.com',
                  'https://mail.google.com',
                  'http://www.mozilla.org']


if len(sys.argv) > 1:
    home = '/home/%s' % sys.argv[1]
else:
    home = '~'
                                    
# Goto Firefox's internal area
path = os.path.expanduser('%s/.mozilla/firefox' % home)
history = 'places.sqlite'
for dir in os.listdir(path):
    print dir
    try:
        os.chdir(os.path.join(path, dir))
        break
    except:
        pass

# Check if places.sqlite is there
print os.listdir('.')
if history in os.listdir('.'):
    history_file = os.path.join(path, dir, history)
    print 'Found history file: %s' % history_file
else:
    print 'Did not find history file in %s' % os.path.join(path, dir)
    import sys; sys.exit() 
    

s = 'strings %s' % history_file       
print s
p = Popen(s, shell=True,
          stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
              
if p.stdout is not None:
    history_string = p.stdout.read().strip()
else:
    print 'History not extracted'
    import sys; sys.exit() 

#print history_string    
    
print 'Google searches:'
for line in history_string.split('\n'):
    idx1 = line.find('www.google')
    if idx1 > -1: 
        idx2 = line[idx1:].find('/search')        
        if idx2 > -1:         
            search_id = line.find('q=')
            tmp = line[search_id+2:].split('&')
            print tmp[0]
        
#import sys; sys.exit()         
print 'Sites visited (in addition to Google)'
for line in history_string.split('\n'):
    if line.startswith('http'):
    
        exclude = False        
        for ex in excluded_sites:
            if line.startswith(ex):
                exclude = True

        if not exclude:
            print line
