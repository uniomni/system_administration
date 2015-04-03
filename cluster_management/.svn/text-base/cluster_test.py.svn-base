"""System test suite of compute nodes

Should be run with an account with passwordless ssh to nodes - e.g. user install

Will store result in logfile.
Can be run as cronjob:

# Run cluster test every 20 minutes
*/20 * * * * monitor /usr/local/bin/cluster_test > /var/tmp/cluster_test_cron.log 2>&1

where it is assumed that /usr/local/bin/cluster_test exists, is executable and has the content
#!/bin/bash

python /etc/system_administration/cluster_management/cluster_test.py $@

"""

from config import nodes, nodes_to_build, logfile as errlogfile
import os

# Log
curdate = os.popen('date').read().strip()
fid = open(errlogfile, 'w')
fid.write(curdate + '\n')
fid.write('RUNNING\n')
fid.close()
os.system('chmod a+w %s 2>/dev/null' % errlogfile)

# Run tests

failed = []
# Test that NAS is mounted on head node
print
logfile = 'head.nas'
s = 'df -kh'
s += ' > %s' % logfile
s += ' 2> /dev/null'
err = os.system(s)

fid = open(logfile)
s = fid.read()
fid.close()
os.remove(logfile)

if s.find(':/nas') >= 0 and s.find(':/volume') >= 0:
    print 'NAS mounted: Head node OK'
else:
    print 'NAS mounted: Head node FAILED'
    failed.append('head')

# Check that uid/gid are mapped correctly (NFS4 issue)
logfile = 'head.uid'

# Check mounted filesystems from alamba
s = 'ls -la'
s += ' > %s' % logfile
s += ' 2> /dev/null'
err = os.system(s)

fid = open(logfile)
s = fid.read()
fid.close()
os.remove(logfile)

if s.find('4294967294') >= 0:
    print 'UID/GID mapping (home): Head node FAILED'
    failed.append(node)
elif s.find('nobody') >= 0:
    print 'UID/GID mapping (home): Head node %s FAILED'
    failed.append('head')
else:
    print 'UID/GID mapping (home): Node node OK'


# Check that uid/gid are mapped correctly to NAS
logfile = 'head.uid'

# Check mounted filesystems from NAS
s = 'ls -la /data_area'
s += ' > %s' % logfile
s += ' 2> /dev/null'
err = os.system(s)

fid = open(logfile)
s = fid.read()
fid.close()
os.remove(logfile)

if s.find('4294967294') >= 0:
    print 'UID/GID mapping (nas): Head node FAILED'
    failed.append('head')
elif s.find('nobody') >= 0:
    print 'UID/GID mapping (nas): Head node FAILED'
    failed.append(node)
else:
    print 'UID/GID mapping (nas): Head node OK'




print
for node in nodes_to_build:
    #print 'Trying to contact %s' % node

    # First try using hostname
    s = 'ping -c 1 %s' % node
    s += '> /dev/null'
    err = os.system(s)
    #print 'err', err

    if err == 0:
        print 'PING: Node %s OK' % node
    else:
        print 'PING: Node %s FAILED' % node
        failed.append(node)

print
# Check ssh among those that could be pinged
for node in nodes_to_build:
    if node in failed: continue

    # First try using hostname
    s = 'ssh %s "hostname"' % node
    s += ' 1> /dev/null'
    s += ' 2> /dev/null'
    err = os.system(s)

    if err == 0:
        print 'SSH: Node %s OK' % node
    else:
        print 'SSH: Node %s FAILED' % node
        failed.append(node)

print
# Check that nodes mount to the NAS
for node in nodes_to_build:
    if node in failed: continue

    logfile = '%s.df' % node

    # Get mounted filesystems
    s = 'ssh %s "df -kh"' % node
    s += ' > %s' % logfile
    s += ' 2> /dev/null'
    err = os.system(s)

    fid = open(logfile)
    s = fid.read()
    fid.close()
    os.remove(logfile)

    if s.find(':/nas') >= 0:
        print 'NAS mounted: Node %s OK' % node
    else:
        print 'NAS mounted: Node %s FAILED' % node
        failed.append(node)


print
# Check that home directory is found
for node in nodes_to_build:
    if node in failed: continue

    logfile = '%s.home' % node

    # Get mounted filesystems
    s = 'ssh %s "pwd"' % node
    s += ' > %s' % logfile
    s += ' 2> /dev/null'
    err = os.system(s)

    fid = open('%s.home' % node)
    s = fid.read()
    fid.close()
    os.remove(logfile)

    if s.find('/home') >= 0:
        print 'Home directory mounted: Node %s OK' % node
    else:
        print 'Home directory mounted: Node %s FAILED' % node
        failed.append(node)


print
# Check that uid/gid are mapped correctly (NFS4 issue)
for node in nodes_to_build:
    if node in failed: continue

    logfile = '%s.uid' % node

    # Check mounted filesystems from alamba
    s = 'ssh %s "ls -la"' % node
    s += ' > %s' % logfile
    s += ' 2> /dev/null'
    err = os.system(s)

    fid = open('%s.uid' % node)
    s = fid.read()
    fid.close()
    os.remove(logfile)

    if s.find('4294967294') >= 0:
        print 'UID/GID mapping (home): Node %s FAILED' % node
        failed.append(node)
    elif s.find('nobody') >= 0:
        print 'UID/GID mapping (home): Node %s FAILED' % node
        failed.append(node)
    else:
        print 'UID/GID mapping (home): Node %s OK' % node


print
# Check that uid/gid are mapped correctly to NAS
for node in nodes_to_build:
    if node in failed: continue

    logfile = '%s.uid' % node

    # Check mounted filesystems from NAS
    s = 'ssh %s "ls -la /data_area"' % node
    s += ' > %s' % logfile
    s += ' 2> /dev/null'
    err = os.system(s)

    fid = open('%s.uid' % node)
    s = fid.read()
    fid.close()
    os.remove(logfile)

    if s.find('4294967294') >= 0:
        print 'UID/GID mapping (nas): Node %s FAILED' % node
        failed.append(node)
    elif s.find('nobody') >= 0:
        print 'UID/GID mapping (nas): Node %s FAILED' % node
        failed.append(node)
    else:
        print 'UID/GID mapping (nas): Node %s OK' % node


#print
# Check that memory is correct
#for node in nodes_to_build:
#    if node in failed: continue
#
#    logfile = '%s.mem' % node
#
#    # Get available physical memory
#    s = 'ssh %s "cat /proc/meminfo"' % node
#    s += ' > %s' % logfile
#    s += ' 2> /dev/null'
#    err = os.system(s)
#
#    fid = open('%s.mem' % node)
#    lines = fid.readlines()
#    fid.close()
#    os.remove(logfile)
#
#    fields = lines[0].split()
#    if fields[0].startswith('MemTotal') and int(fields[1]) > 32000000:
#        print '32 GB memory: Node %s OK' % node
#    else:
#        print '32 GB memory: Node %s FAILED' % node
#        failed.append(node)

print
# Check that date and time is in sync
fid = os.popen('date')

# Format: Thu Nov 19 18:21:04 WIT 2009
refdate = fid.read().strip()
reffields = refdate.split()
reftime = reffields[3].split(':')

# convert time to absolute seconds:
ref_seconds = int(reftime[0])*3600 + int(reftime[1])*60 + int(reftime[2])
fid.close()
#print 'Reference date', refdate

print 'Head node reference date: %s' % refdate
for node in nodes_to_build:
    if node in failed: continue

    logfile = '%s.date' % node

    # Get timestamp
    s = 'ssh %s "date"' % node
    s += ' > %s' % logfile
    s += ' 2> /dev/null'
    err = os.system(s)

    fid = open('%s.date' % node)
    date = fid.read().strip()
    datefields = date.split()
    fid.close()
    os.remove(logfile)

    time = datefields[3].split(':')
    # convert time to absolute seconds:
    seconds = int(time[0])*3600 + int(time[1])*60 + int(time[2])


    # Ascertain equality except for seconds
    equal = True
    for i in range(len(datefields)):
        if not equal: break

        if i == 3:
            # Compare time separately
            if abs(seconds - ref_seconds) > 60:  # Allow up to 60 seconds difference (in case nodes are busy)
                equal = False
                break
        else:
            if datefields[i] != reffields[i]:
                equal = False
                #print datefields[i], reffields[i]

    if equal:
        print 'Date %s: Node %s OK' % (date, node)
    else:
        print 'Date %s: Node %s FAILED - reference date is %s' % (date, node, refdate)
        failed.append(node)




# Report


N = len(failed)
curdate = os.popen('date').read().strip()
fid = open(errlogfile, 'w')
fid.write(curdate + '\n')
print
if N > 0:
    fid.write('ERROR\n')
    print 'Number of failed nodes: %d' % N
    print 'Failed nodes'
    for node in failed:
        print node
        fid.write(node + '\n')

else:
    print 'Cluster passed all tests OK'
    fid.write('OK\n')
fid.close()
os.system('chmod a+w %s 2>/dev/null' % errlogfile)

