"""Run all configuration scripts in order.
"""

import os
from config import nodes_to_build

curdir = os.getcwd()

for script in ['configure_server.py', 
               'build_clients.py',
               'configure_clients.py',
               'restart_services.py',
               'synchronise_clients.py']:
    os.chdir(curdir)
    s = 'Executing %s' % script
    dashes = '-'*len(s)
    print 
    print dashes
    print s
    print dashes
    execfile(script)



print
print 'Done - following PXE clients have been rebuilt:'
for hostname in nodes_to_build:
    print hostname + ' ',
print
