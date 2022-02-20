"""Automatic backup of files to using rsync and hardlink snapshots

python create_snapshot.py [options] <dir1> <dir2> ...

where <dir1> <dir2> ... is a list of directories that will be backed up.

Options are

  -h, --help: Show usage string
  -d, --destination: Nominate destination directory for snapshots
  -m, --mode: Select snapshot mode (sync, tag, weed, stat or save). See below.

  
The argument to --mode or -m are

sync
    Performs the incremental rsync of selected directories
    Can be run frequently e.g. every half hour

tag
    Rotates snapshots to retain older versions
    Should be run every 2 or 4 hours

weed
    Deletes superfluous snapshots.
    Should be run daily during a quiet time

stat
   Outputs statistics about disk space usage

save
   Make nominated snapshot persistent by copying and 
   appending user specified tag     

   
Without --mode create_snapshot.py will assume 'sync' action.

A range of file patterns such as *.o and *~ specified in exclude_pattern in
the associated config.py file are excluded from the snapshot to conserve space.


Examples
python create_snapshot.py --destination=/backup --mode=sync /etc /home
python create_snapshot.py --destination=/backup --mode=tag
python create_snapshot.py --destination=/backup --mode=weed
python create_snapshot.py --destination=/backup --mode=stat
python create_snapshot.py --destination=/backup --mode=save snapshot.2010-02-05T08-33-01 initial_state



The script can be executed either manually or
as a cron job. E.g

# --------------------------------------------------------------
# Create regular snapshots of selected filesystems
# Make sure /etc/system_administration has been updated with svn
# --------------------------------------------------------------

# Update latest snapshot every hour
3 * * * * root nice python /etc/system_administration/backup/create_snapshot.py --destination=/backup --mode=sync /home /etc > /var/log/snapshot_sync.lastlog 2>&1

# Make snapshot of backup tree every two hours  
33 0-23/2 * * 1-7 root nice python /etc/system_administration/backup/create_snapshot.py --destination=/backup --mode=tag > /var/log/snapshot_tag.lastlog 2>&1

# Weed-out superfluous snapshots every night 2:43
43 2 * * * root nice python /etc/system_administration/backup/create_snapshot.py --destination=/backup --mode=weed > /var/log/snapshot_weed.lastlog 2>&1

# Get statistics every morning 5:45
45 5 * * * root nice python /etc/system_administration/backup/create_snapshot.py --destination=/backup --mode=stat > /var/log/snapshot_stat.lastlog 2>&1

"""

from config import include_list, exclude_list, delay, tmpfile_basename, logfile, lockfile
from config import use_gnu, latest_snapshot_dir, snapshot_dir, dryrun, verbose, allowed_modes
import sys, time, os, string, getopt



def usage():
    print('Usage:')
    print('python create_snapshot.py [options] <dir1> <dir2> ...')
    print('Options:')
    print('  -h, --help: Show usage string')
    print('  -d, --destination: Nominate destination directory for snapshots')
    print('  -m, --mode: sync (default), tag, weed, save or stat.')
  
    
#------------------------------------
# The program
#------------------------------------

def make_timeslot(time_tuple):
  """Return [year, month, week, day, hour]
     Must be organised from slow to fast measure.
  """
  return [time_tuple[0], time_tuple[1], int(time_tuple[7] / 7),\
          time_tuple[2], time_tuple[3]]

# Has to be consistent with make_timeslot for reporting purposes!
timeslot_names = ['yearly', 'monthly', 'weekly', 'daily', 'hourly']




def makedir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well

    Based on            
    http://code.activestate.com/recipes/82465/
    
    Note os.makedirs does not silently pass if directory exists.
    """
    
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        msg = 'a file with the same name as the desired ' \
            'dir, "%s", already exists.' % newdir
        raise OSError(msg)
    else:
        head, tail = os.path.split(newdir)
        if head and not (os.path.isdir(head) or os.path.islink(head)):
            makedir(head)
        if tail:
            os.mkdir(newdir)


def snapshot(destination, mode, snapshot_dirs):          
    """Snapshot machinery
    """

    t_start = time.time()

    # Form destination dir based on current time stamp
    time_tuple = time.localtime(t_start)
    time_stamp = time.strftime('%Y-%m-%dT%H-%M-%S', time_tuple) # ISO 8601 time stamp (except colons)

    # Equip destination with timestamp etc
    target = os.path.join(destination, snapshot_dir) + '.' + time_stamp
    most_recent_hardlink = os.path.join(destination, latest_snapshot_dir)
    tmpfile = tmpfile_basename + '.' + time_stamp

    if use_gnu:
      copycmd = 'cp -al %s %s' % (most_recent_hardlink, target)
    else:  
      copycmd = 'mkdir %s; cd %s && find . -print | cpio -dpl %s'\
                % (target, most_recent_hardlink, target)

    # Create destination if necessary
    makedir(destination)  


    if mode in ['sync', 'tag']:
        # Check that previous snapshot has finished
        try:
            fid = open(lockfile,'r')
            backup_time = fid.readline().strip() 
            fid.close()
            backup_in_progress = True
        except:
            backup_in_progress = False
      
        if backup_in_progress:
            s = '%s: Rotating snapshots still in progress since %s.\n'\
                  % (time_stamp, backup_time)
            s += 'Please wait till previous snapshot has completed.\n'
            s += 'If this is wrong, please delete %s and try again.' % lockfile 
            raise Exception(s)
        else:
            pass
          
      
        # Make lock
        if verbose > 0: print('Making lock file %s' % lockfile)
        fid = open(lockfile, 'w')
        fid.write(mode + ':' + time_stamp + '\n')
        fid.close()



    # Write to log file
    try:
        fid = open(logfile, 'a')
        fid.write('Started snapshot %s at %s\n' %(mode, time.asctime()))
        fid.close()
    except:
        pass     

    # Create target dir if necessary
    makedir(most_recent_hardlink)
      
      
    
    # Rsync stuff
    if mode in ['sync', 'tag']:

        # Form include/exclude string and options
        exclude_string = ''
        for pattern in exclude_list:
            exclude_string += '--exclude "%s" ' %pattern  
        
        include_string = ''
        for pattern in include_list:
            include_string += '--include "%s" ' %pattern  
        
        rsync_long_options = '%s %s --delete --delete-excluded --delete-after'\
                             %(include_string, exclude_string)
        
        if verbose == 2:
            rsync_short_options = '-azv'
        else:
            rsync_short_options = '-az'
        

        
        # Start backing up
        for dir in snapshot_dirs:
            cmd = 'rsync %s %s  %s %s'\
                %(rsync_short_options, rsync_long_options, dir,\
                    most_recent_hardlink)      
            
            if verbose > 0:
                print(cmd)

            if not dryrun:
                exitcode = os.system(cmd)
                if exitcode != 0 and verbose > 0:
                    print('\nWARNING (snapshot): Problems copying directory %s to %s'\
                          % (dir, most_recent_hardlink))
                    print ('                  This can for example happen if user')
                    print ('                  is not allowed to read all of %s or if it does not exist' % dir)
        
        # Update time stamp on newly created snapshot
        cmd = 'touch %s' % most_recent_hardlink
        exitcode = os.system(cmd)
        
        # Make snapshot read only
        cmd = 'chmod -R a-w %s' % most_recent_hardlink
        print(cmd)
        exitcode = os.system(cmd)        
        
        if verbose > 0: print('rsync completed in %d seconds' % (time.time() - t_start))


    # Tag
    if mode in ['tag']:
        
        t_snap = time.time()
       
        # Make hard links from  most recent backup to name with time stamp
        cmd = '%s' % copycmd

        if verbose > 0:
            print(cmd)
     
        exitcode = os.system(cmd)
       
       
        if verbose > 0: print('hardlink rotation completed in %d seconds'\
                              % (time.time() - t_snap))



    # Weed
    if mode in ['weed']:

       # House keeping - weed out among older snapshots
       t_weed = time.time()   
       current_timeslot = make_timeslot(time_tuple)
       

       # Create a dictionary for each timeslot
       timedict = []
       for c in current_timeslot:
           timedict.append({})  
       keeplist = []   
       
       # Get all backup directories and extract their time stamps
       cmd = '%s > %s' % ('ls %s' % destination, tmpfile)

       exitcode = os.system(cmd)
       fid = open(tmpfile, 'r')
       for line in fid.readlines():
           filename = line.strip()
       
           field_list = filename.split('.')  # Extract extension (time stamp)
           processed = 0
           if len(field_list) > 1:
               stamp = field_list[1]
               if stamp is not None:
                   try:
                       time_tuple = time.strptime(stamp, '%Y-%m-%dT%H-%M-%S')
                   except:
                       print('Warning:' + stamp + ' could not be parsed')
                       continue
       
                   # Organise files in the various time slots
                   # ordered as year, month, week, day, hour
                   # as specified in make_timeslot
                   timeslot = make_timeslot(time_tuple)
       
                   for i in range(len(timeslot)):
                       if timeslot[i] < current_timeslot[i] - delay[i]:
                           # File is older than current time slot - delay,
                           # put it into appropriate slot.
                           #if not timedict[i].has_key(timeslot[i]):
                           if timeslot[i] not in timedict[i]:
                               timedict[i][timeslot[i]] = {}
                           timedict[i][timeslot[i]][filename] = time.mktime(time_tuple)
                           processed = 1             
                           break  # Do not enter file into more than one slot
                 
           if not processed: keeplist.append(filename)
         
         
       # Keep only the newest from each list
       delete_files = []
       i = 0
       for ttt in timedict:
           for flist in ttt.values():
               if len(flist) > 0:
                   # Sort
                   V = flist.values()
                   F = flist.keys()
                   A = list(zip(V, F))
                   A.sort()
                   keepfile = A[-1][1]
                   tobe_deleted = list(map(lambda x: x[1], A[:-1]))
                 
                   print('Expired time slot (%s)' %timeslot_names[i])
                   if len(tobe_deleted) > 0:
                       print('  Delete: ', tobe_deleted)
                   print('  Keep:   ', keepfile)
                   print()
                   keeplist.append(keepfile)

                   delete_files += tobe_deleted # Accumulate
               
           i += 1
       

       print('To be deleted:')
       print(delete_files)
       print()
       print('To be kept:')
       print(keeplist)
       print()
       
       
       # Delete superfluous files
       if len(delete_files) > 0:
           delete_string = ' '.join(delete_files)
           cmd = 'cd %s; /bin/rm -rf %s' % (destination, delete_string)

           if verbose > 0: print(cmd)
           if not dryrun: os.system(cmd)
       
           if verbose > 0: print('superfluous files deleted in %d seconds'\
              %(time.time() - t_weed))




    # Statistics
    if mode in ['stat']:

       # Get some stats on disk usage
       t_stats = time.time()   

       # Number of backups
       cmd = '%s > %s' %('ls %s' % destination, tmpfile)
       exitcode = os.system(cmd)

       fid = open(tmpfile, 'r')
       files = fid.readlines()
       fid.close()
       
       print('You currently have %d backups' %(len(files)))


       cmd = '%s > %s' % ('du -sDh %s/latest_snapshot' % destination, tmpfile)
       if verbose: print(cmd)
       exitcode = os.system(cmd)
       cmd = '%s >> %s' %('du -sDh %s' % destination, tmpfile)
       if verbose: print(cmd)   
       exitcode = os.system(cmd)



       fid = open(tmpfile, 'r')
       lines = fid.readlines()
       fid.close()

       if len(lines) == 2:
           size1 = lines[0].strip().split()[0]
           size2 = lines[1].strip().split()[0]     
         
           print('Size of latest backup: %s bytes' % size1)
           print('Size of all backups:   %s bytes' % size2)      


       if verbose > 0: print('Statistics obtained in %d seconds'\
             %(time.time() - t_stats))



    try:
        fid = open(logfile, 'a')             
        fid.write('Finished backup %s in %d seconds at %s\n'\
                    %(mode, time.time()-t_start,time.asctime()))
        fid.close()
    except:
        print('WARNING: Could not open log file %s. Do you have write permissions?' % logfile)
      

    if mode in ['sync', 'tag']:
        # Remove lockfile  
        os.system('/bin/rm -r %s' % lockfile)


def save_snapshot(destination, snapshot_name, tag):
    """Copy named snapshot and append tag to it 
    """
    
    snapshot = os.path.join(destination, snapshot_name)
    target = snapshot + '.' + tag
    
    if use_gnu:
        copycmd = 'cp -al %s %s' % (snapshot, target)
    else:  
        copycmd = 'mkdir %s; cd %s && find . -print | cpio -dpl %s'\
            % (target, snapshot, target)
    
    print(copycmd)
    os.system(copycmd)
      
      
if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hd:m:', ['help', 'destination=', 'mode='])
    except getopt.GetoptError(err):
        # print help information and exit:
        print(str(err))
        usage()
        sys.exit() 
        
    destination = '.'
    mode = 'sync'
    for o, a in opts:
        if o == '-v':
            verbose = True
        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-d', '--destination'):
            destination = a
        elif o in ('-m', '--mode'):
            msg = 'Unknown option for mode: %s. Options are %s ' % (str(a), allowed_modes)
            assert a in allowed_modes, msg
            mode = a            
        else:
            msg = 'Unknow option %s' % str(o)
            raise Exception(msg)

    arguments = []    
    for dir in args:
        arguments.append(dir)


    if mode == 'sync':
        msg = 'At least one directory must be specified for sync mode'
        assert len(arguments) > 0, msg
    elif mode == 'save':
        msg = 'Mode "save" requires valid snapshot directory and user specified tag'
        assert len(arguments) == 2, msg    
        snapshot_name = arguments[0]
        tag = arguments[1]
        save_snapshot(destination, snapshot_name, tag)
        sys.exit() 
    else:
        msg = 'Modes tag, weed and stat do not require additional arguments. '
        msg += 'You specified %s' % str(arguments)
        assert len(arguments) == 0, msg     
        
    
    snapshot(destination, mode, arguments)
