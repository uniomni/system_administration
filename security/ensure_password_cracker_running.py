"""Check that the password cracker john is running.
If not start it.

This script should be run from a cronjob as root:

# --------------------------------------------------------------
# Ensure that password cracker is always running
# --------------------------------------------------------------
53 1 * * * root python /etc/system_administration/security/ensure_password_cracker_running.py > /var/log/ensure_pwc_running.log 2>&1



NOTE: This script assumes that the john executable is /usr/local/jrt/john
and also that run script is located either locally or in /etc/system_administration/security
"""

import os
from subprocess import Popen, PIPE


p = Popen('ps aux | grep john', shell=True,
          stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
              
lines = p.stdout.readlines()

running = False
for line in lines:
    if '/usr/local/jrt/john' in line:
        print 'John is running'
        running = True
        

if not running:
    print 'John is not running - restarting'
    s = '/usr/local/jrt/john /etc/shadow >/var/log/john.log 2>/var/log/john.err &'
    print s
    os.system(s)

