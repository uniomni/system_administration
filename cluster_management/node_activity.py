"""Poor Mans Ganglia - report activity on each node in a cluster

Run e.g. as
python node_activity.py
or for automatic updating
watch -n 60 python node_activity.py

It assumed that nodes have passwordless ssh access

NOTE: Watch doesn't always clear the screen so old info may linger. Running clear between jobs doesn't seem to work either.
Best to just restart watch if this happens
"""

import re
import os
import shlex
import socket
from operator import itemgetter
from subprocess import Popen, PIPE
from threading import Timer
from config import nodes


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

def generate_userlist(users, nodes, users_overloading_nodes):
    """Generate list of users for active processes.

    Also update dictionary of users running on overloaded nodes
    """

    userlist = ''
    for key in users:
        user, cmd = key

        # List users and programs for each node
        cpu_usage = users[key]['cpu']
        n = users[key]['procs']
        if cpu_usage > 10:
            #userlist += '%s (%s x %i, %.0f), ' % (user, cmd, n, cpu_usage/100.)
            userlist += '%s (%s x %i), ' % (user.ljust(8), cmd, n)

            # Record users overloading nodes
            if load > 8.5:
                if user in users_overloading_nodes:
                    users_overloading_nodes[user][nodes] = load
                else:
                    users_overloading_nodes[user] = {nodes: load}

    if len(userlist) > 2:
        userlist = userlist[:-2]

    return userlist

# Get CPU usage
print 'Requesting load statistics for each node'
print '----------------------------------------'
L = []
cpu_usage = {}
nodes = nodes.keys()
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

        key = (user, prg)
        if key in users:
            users[key]['cpu'] += cpu
            users[key]['mem'] += mem
            users[key]['procs'] += 1
        else:
            users[key] = {'cpu': cpu,
                          'mem': mem,
                          'dur': dur,
                          'procs': 1}

    stats = (load1, node, users)
    if node == headnode:
        headstats = stats
    else:
        L.append(stats)


print
print 'Sorted by average load the last 1 minute (from idle to busy)'
print
print 'Node     Load      Users    (command x N)'
print '---------------------------------------------------------------'

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
        if load > 8.5:
            msg = 'Over'
        elif load > 7:
            msg = 'Full'
        elif load > 4:
            msg = 'Busy'
        elif load > 1:
            msg = 'Free'
            free_nodes.append(nodes[i])
        else:
            msg = 'Idle'
            free_nodes.append(nodes[i])

    userlist = generate_userlist(users[i], nodes[i], users_overloading_nodes)
    print '%s %.0f (%s)  %s' % (nodes[i].ljust(8), load, msg, userlist)


if len(users_overloading_nodes) > 0:
    print
    print
    print 'WARNING: The following users are running on overloaded nodes '
    print '         reducing the overall performance. Consider reducing '
    print '         the total number of jobs to a maximum of 8 per node.'
    print
    print 'User    Nodes (load)'
    print '--------------------'
    for user in users_overloading_nodes:
        nodelist = ''
        for node in users_overloading_nodes[user]:
            nodelist += '%s (%.1f), ' % (node, users_overloading_nodes[user][node])
        if len(nodelist) > 2:
            nodelist = nodelist[:-2]
        print '%s: %s' % (user, nodelist)

# Check headnode activity
#print head
if headstats is not None and headstats[0] > 0.5:
    nodes = headstats[1]
    users = headstats[2]
    userlist = generate_userlist(users, nodes, users_overloading_nodes)
    print
    print 'WARNING: Headnode is running at load %.0f: %s' % (headstats[0], userlist)
    print 'Consider moving jobs to compute nodes'

# Report on available
if len(free_nodes) > 0:

    free_nodes = nodesort(free_nodes)
    s = ''
    for i, node in enumerate(free_nodes):
        s += '%s' % node
        if i < len(free_nodes) - 2:
            s += ', '
        elif i == len(free_nodes) - 2:
            s += ' and '

    print
    print 'There is spare capacity on %s' % s


