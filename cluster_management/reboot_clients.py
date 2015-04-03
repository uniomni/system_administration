"""Reboot clients listed in config.py
"""
import os, time
from config import nodes_to_build 

password = raw_input('Password? ')
pwname = 'horlchkt8739087kkknoe9'
fid = open(pwname, 'w')
fid.write(password + '\n')
fid.close()

for node in nodes_to_build:
    s = 'ssh %s "sudo reboot" < %s' % (node, pwname)
    print s
    os.system(s)
    print 'Pausing'
    time.sleep(15)

os.remove(pwname)

print 'Give last node a two minutes to complete its boot - then run ping_clients.py'
time.sleep(120)

execfile('ping_clients.py')
