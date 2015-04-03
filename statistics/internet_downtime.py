"""Regularly verify internet connectivity and report downtime
Run as sudo e.g. from a cronjob

# --------------------------------------------------------------
# Regular internet connectivity check
# --------------------------------------------------------------

*/5 * * * * root nice python /etc/system_administration/statistics/internet_downtime.py

"""

from config import internet_logfile, internet_statfile
import os, time, commands


cmd = 'ping -c 1 www.google.com'
res = commands.getoutput(cmd)

cmd = 'echo `date +%Y%m%d-%H%M%S`:'
if res.find('bytes from') > 0:
    cmd += ' UP >> %s' % internet_logfile
else:
    cmd += ' DOWN >> %s' % internet_logfile

os.system(cmd)    
    

# Generate uptime report
fid = open(internet_logfile)
lines = fid.readlines()
fid.close()

# Find consecutive periods of downtime
fid = open(internet_statfile, 'w')
down_period = False
for line in lines:
    time_stamp, status = line.strip().split(':')
    t = time.mktime(time.strptime(time_stamp, '%Y%m%d-%H%M%S'))
    status = status.strip()
    
    #print time_stamp, status
    if status == 'DOWN' and not down_period:
        # Record start of down period    
        down_period = True
        t_start = time_stamp
        t0 = t
        
        
    if status == 'UP' and down_period:
        # Record end of down period    
        down_period = False
        t_end = time_stamp        
        duration = t-t0
        
        hours = duration // 3600
        minutes = duration % 3600 // 60
        seconds = duration % 60
        
        if hours == 0:
            if minutes == 0:
                time_string = '%i seconds' % seconds
            else:
                time_string = '%i minutes' % minutes
        else:
            time_string = '%i hours %i minutes' % (hours, minutes)        
                
        fid.write('Internet downtime for %s from %s to %s\n' % (time_string, t_start, t_end))
        
        
fid.close()    
