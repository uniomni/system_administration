from config import nodes, nodes_to_build
import os

# Should be run with an account with passwordless ssh to nodes - e.g. user install

failed = []
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

    fid = open('%s.df' % node)
    s = fid.read()
    fid.close()
    os.remove(logfile)

    if s.find(':/nas') >= 0:
        print 'NAS mount: Node %s OK' % node
    else:
        print 'NAS mount: Node %s FAILED' % node
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
        print 'Home directory: Node %s OK' % node
    else:
        print 'Home directory: Node %s FAILED' % node
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
        print 'UID/GID mapping of /home: Node %s FAILED' % node
        failed.append(node)
    elif s.find('nobody') >= 0:
        print 'UID/GID mapping of /home: Node %s FAILED' % node
        failed.append(node)
    else:
        print 'UID/GID mapping of /home: Node %s OK' % node


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


print
# Check that memory is correct
for node in nodes_to_build:
    if node in failed: continue

    logfile = '%s.mem' % node

    # Get available physical memory
    s = 'ssh %s "cat /proc/meminfo"' % node
    s += ' > %s' % logfile
    s += ' 2> /dev/null'
    err = os.system(s)

    fid = open('%s.mem' % node)
    lines = fid.readlines()
    fid.close()
    os.remove(logfile)

    fields = lines[0].split()
    if fields[0].startswith('MemTotal') and int(fields[1]) > 32000000:
        print '32 GB memory: Node %s OK' % node
    else:
        print '32 GB memory: Node %s FAILED' % node
        failed.append(node)

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

    # Get available physical memory
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
            if abs(seconds - ref_seconds) > 10:  # Allow up to 10 seconds difference
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


N = len(failed)
print
print 'Number of failed nodes: %d' % N
if N > 0:
    print 'Failed nodes'
    for node in failed:
        print node


