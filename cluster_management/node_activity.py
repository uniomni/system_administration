"""Poor Mans Ganglia - report activity on each node in a cluster

Run e.g. as
python node_activity.py
or for automatic updating
watch -n 60 python node_activity.py

It assumed that nodes have passwordless ssh access

NOTE: Watch doesn't always clear the screen so old info may linger. Running clear between jobs doesn't seem to work either.
Best to just restart watch if this happens


It is handy to create the executable /usr/local/bin/node_activity with content
#!/bin/bash

python /etc/system_administration/cluster_management/node_activity.py $@

"""

import re
import os
import shlex
import socket
from operator import itemgetter
from subprocess import Popen, PIPE
from threading import Timer
from config import nodes, nodes_to_build, logfile, number_of_processors_per_node

def pipe(cmd, verbose=False):
    """Simplification of the new style pipe command

    One object p is returned and it has
    p.stdout, p.stdin and p.stderr

    If p.stdout is None an exception will be raised.


    Example
    try:
        p = pipe('whoami')
    except:
        username = 'unknown'
    else:
        username = p.stdout.read().strip()
    """

    if verbose:
        print cmd

    def kill_proc():
        print 'Command "%s" timed out - killing.' % cmd
        p.kill()
        p.stdout = None  # Cause check below to raise Exception
        os.system('stty echo')  # All this killing causes echo to get lost so need to restore it

    p = Popen(shlex.split(cmd), shell=False,  # Cannot kill process when shell is True
              stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

    # Setup time-out e.g. in case ssh asks for a password
    t = Timer(20, kill_proc)
    t.start()
    p.wait()

    if p.stdout is None:
        msg = 'Piping of command %s could be executed' % cmd
        raise Exception(msg)

    # Cancel the time-out and return
    t.cancel()
    return p


def nodesort(nodes):
    """Sort nodes based on their numerical values
    """

    #nodes.sort()  # Naive
    #nodes = sorted(nodes, key=lambda x: int(x[4:]))  # Simple
    nodes = sorted(nodes, key=lambda x: int(re.findall('([0-9]+)', x)[0]))  # General

    return nodes

def generate_userlist(users, load, nodes, users_overloading_nodes):
    """Generate list of users for active processes.

    Also update dictionary of users running on overloaded nodes
    """

    userlist = ''
    for key in users:
        user, cmd = key

        # List users and programs for each node
        cpu_usage = users[key]['cpu']
        mem_usage = users[key]['mem']
        n = users[key]['procs']
        minutes = users[key]['min']
        if cpu_usage > 10:
            #userlist += '%s (%s x %i, %.0f), ' % (user, cmd, n, cpu_usage/100.)
            userlist += '%s (%s x %i, %2i, %ih %im), ' % (user.ljust(8), cmd, n, mem_usage, minutes / 60, minutes % 60)
            # Record users overloading nodes
            if load > 105:
                if user in users_overloading_nodes:
                    users_overloading_nodes[user][nodes] = load
                else:
                    users_overloading_nodes[user] = {nodes: load}

    if len(userlist) > 2:
        userlist = userlist[:-2]

    return userlist

# Get CPU usage
print '--------------------------------------------------------------------------'
print 'Load statistics for cluster nodes sorted by average load the last 1 minute'
print
print 'Node     Load %      Users    (command x N, Mem %, Time)'
print '--------------------------------------------------------------------------'

L = []
cpu_usage = {}
#nodes = nodes.keys()
nodes = nodes_to_build
nodes =  nodesort(nodes)

exceptions = 'grep -v root | grep -v syslog | grep -v gdm | grep -v syslog | grep -v daemon | grep -v statd'

headnode = socket.gethostname()
headstats = None
for node in nodes + [headnode]:

    cmd = 'ssh %s top -b -n 1 | %s | head -200' % (node, exceptions)
    try:
        p = pipe(cmd)
    except:
        print 'Could not connect to node %s' % node
        continue

    # Get load
    lines = p.stdout.readlines()
    if lines is None or len(lines)==0:
        print 'Could not read from node %s' % node
        continue

    line = lines[0].strip()
    #print '%s %s' % (node.ljust(7), line)
    # Extract CPU loads
    loads = line.split(':')[-1].split(',')
    load1 = round(float(loads[-3]), 0)
    load5 = round(float(loads[-2]), 0)
    load15 = round(float(loads[-1]), 0)

    # Get users
    users = {}
    for line in lines[7:]:
        fields = line.strip().split()
        if len(fields) == 0:
            continue

        user = fields[1].strip()
        cpu = int(fields[8])
        mem = float(fields[9])
        dur = fields[10]
        prg = fields[11]

        # Get time in minutes
        try:
            minutes = int(dur.split(':')[0])
        except ValueError:
            # Take care of weird entries like
            # 28401 vanpuk    20   0 1134m 453m  24m S 9999  1.4  5197858h firefox-bin
            continue


        # Record stats per user
        key = (user, prg)
        if key in users:
            users[key]['cpu'] += cpu
            users[key]['mem'] += mem
            users[key]['procs'] += 1
            users[key]['min'] = max(minutes, users[key]['min'])
        else:
            users[key] = {'cpu': cpu,
                          'mem': mem,
                          'min': minutes,
                          'procs': 1}

    # Convert load to pct and record node, users as well
    stats = (load1*100/number_of_processors_per_node, node, users)
    if node == headnode:
        headstats = stats
    else:
        L.append(stats)


# Swarzian transform
L = sorted(L, key=itemgetter(0))
if headstats is not None:
    L += [headstats]
loads = [x[0] for x in L]
nodes = [x[1] for x in L]
users = [x[2] for x in L]

users_overloading_nodes = {}
free_nodes = []

# Print out
for i, load in enumerate(loads):

    if nodes[i] == headnode:
        msg = 'Head'
    else:
        if load > 105:
            msg = 'Over'
        elif load > 85:
            msg = 'Full'
        elif load > 50:
            msg = 'Busy'
        elif load > 10:
            msg = 'Free'
            free_nodes.append(nodes[i])
        else:
            msg = 'Idle'
            free_nodes.append(nodes[i])

    userlist = generate_userlist(users[i], load, nodes[i], users_overloading_nodes)
    print '%s %3i (%s)  %s' % (nodes[i].ljust(8), load, msg, userlist)


if len(users_overloading_nodes) > 0:
    print
    print 'WARNING: The following users are running on overloaded nodes reducing the overall performance. '
    print '         Consider reducing the total number of jobs to a maximum of %i per node.' % number_of_processors_per_node
    #print
    #print 'User    Nodes (load)'
    #print '--------------------'
    for user in users_overloading_nodes:
        nodelist = ''
        for node in users_overloading_nodes[user]:
            nodelist += '%s (%.0f), ' % (node, users_overloading_nodes[user][node])
        if len(nodelist) > 2:
            nodelist = nodelist[:-2]
        print '         %s: %s' % (user, nodelist)

# Check headnode activity
load = headstats[0]
if headstats is not None and load > 50:
    nodes = headstats[1]
    users = headstats[2]
    userlist = generate_userlist(users, load, nodes, users_overloading_nodes)
    print
    print 'WARNING: Headnode is running at load %i%%: %s' % (load, userlist)
    print '         Consider moving jobs to compute nodes'

# Report on available nodes
if len(free_nodes) > 0:

    free_nodes = nodesort(free_nodes)
    s = ''
    for i, node in enumerate(free_nodes):

        # Line break
        if 0 < i < len(free_nodes) - 1 and i % 10 == 0:
            s += '\n                           '

        # Add to free node list
        s += '%s' % node
        if i < len(free_nodes) - 2:
            s += ', '
        elif i == len(free_nodes) - 2:
            s += ' and '

    print
    print 'There is spare capacity on %s' % s
else:
    print
    print 'Cluster is fully utilised'


# Check uptime and if cluster test (ping_clients.py) has been run succesfully (by cron)
print
p = pipe('uptime')
fields = p.stdout.read().split()
if ':' in fields[2]:
    # After a fresh reboot uptime will be something like 2:34
    days_up = 1
else:
    # Later it'll be reported as a whole number of days
    days_up = int(fields[2])
print 'Headnode has been up for %i %s.' % (days_up, fields[3][:-1]),

try:
    fid = open(logfile)
except:
    print 'Could not open logfile %s' % logfile
else:
    lines = fid.readlines()
    if len(lines) >= 2:
        timestamp = lines[0].strip()
        result = lines[1].strip()

        if 'OK' in result:
            print 'Cluster passed all tests most recently on %s' % timestamp
        elif 'ERROR' in result:
            print 'Errors were found on %s. Please check %s or run cluster_test to investigate.' % (logfile, timestamp)
        elif 'RUNNING' in result:
            print 'Cluster test started on %s and should normally complete within a few minutes.' % timestamp
        else:
            print 'Could not determine result from cluster system test. I got %s. Please check %s' % (result, logfile)
    else:
        print 'Could not determine result from cluster system test. Please check %s' % logfile


celeb_days = [40, 50, 60, 100, 150, 200, 201, 202, 203, 250, 500, 1000]
for d in celeb_days:
    if days_up == d:
        #s = 'SEKARANG SELAMATAN %i HARI KELAHIRAN ALAMBA - SEMUA ORANG BERGEMBIRA!!!' % d
        #s = 'SEKARANG SELAMATAN %i HARI SEJAK JONO MEMPERBAIKI ALAMBA - SEMUA ORANG BERGEMBIRA!!!' % d
        s = 'SELAMAT %i HARI ALAMBA - SEMUA ORANG BERGEMBIRA!!!' % d

        print
        print '-' * len(s)
        print s
        print '-' * len(s)

if 200 < days_up < 204:
    s = 'ALAMBA SUDAH HIDUB LEBIH DARI 200 HARI - SEMUA ORANG BERGEMBIRA!!!'

    print
    print '-' * len(s)
    print s
    print '-' * len(s)


# Show disk usage of selected filesystems:
p = pipe('df -h')
lines = p.stdout.readlines()
header = lines[0].strip()  # Used to get spacing from df -h
idx1 = header.find('Size')
idx2 = header.find('Mounted')
print
print 'Directory       ' + header[idx1:idx2]
filesystems = ['/model_area', '/data_area', '/snapshot_area', '/TsuDAT', '/OPENSTACK']
for filesystem in filesystems:
    for line in lines:
        if filesystem in line and ':' not in line:
            text = line.strip()
            fields = text.split()
            idx = text.find('%')
            print fields[-1].ljust(15),
            print text[:idx+1]

