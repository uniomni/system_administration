"""Configuration parameters for create_snapshot.py
"""

# These are the allowed keywords on the command line
allowed_modes = ['sync', 'tag', 'weed', 'stat', 'save']

# General exclude patterns. See man rsync for details on usage.
exclude_list = ['*~', '.*~', '#*#', '.#*', '*.o', '*.so']
exclude_list += ['.mozilla', '.Trash', '.gvfs', '.gconf', '.gconfd', '.cache']
exclude_list += ['/run']

# Exclude everything in /var except log and spool/mail
#exclude_list += ['/var/*', '/var/spool/*', 'cache']
include_list = []

# Delays (in each timeslot: year, month, week, day, hour) before
# old snapshots get weeded out. For example [0,0,0,0,0].
delay      = [1,1,0,0,0]

# System filenames
tmpfile_basename = '/tmp/snapshot_files' # Temporary storage on local host
logfile = '/var/log/snapshot.log'
lockfile = '/var/lock/snapshot.lock'
latest_snapshot_dir = 'latest_snapshot'
snapshot_dir = 'snapshot' # This will get timestamped

# General configuration - this will probably never change
use_gnu = 1     # Set to 1 only if using GNU on remote system
dryrun = 0     # Don't actually do it - for testing purposes
verbose = 2     # Verbose output. 0: Nothing, 1: Some, 2: Everything

