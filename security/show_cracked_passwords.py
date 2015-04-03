"""Show cracked passwords
"""

import os
s = 'sudo /usr/local/jrt/john --show /etc/shadow'
print 
print s
os.system(s)
