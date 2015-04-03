"""This is the rsync command to backup entire head node
"""

import os 

target = '/scratch_area/headnode_backup'


cmd = 'rsync -avz --exclude=/data_area --exclude=/scratch_area --exclude=/model_area --exclude=/snapshot_area --exclude=/proc --exclude=/cdrom / %s' % target

print cmd
os.system(cmd) 
