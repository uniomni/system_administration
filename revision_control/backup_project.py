"""Backup all Subversion/TRAC projects

The location of dumps is determined in config.py in the variable backup_dir

This script is intended to be run regularly as a cronjob.
"""

from config import svn_home, trac_home, backup_dir, svndumpname, tracdumpname, errlog, logfile
from utilities import consolidate_configuration_files, run, makedir, header
from os.path import join
import os
import sys
import time


def usage():
    print 'Usage:'
    print 'sudo python backup_project.py <project>'
    print 'where <project> is the name of an existing subversion/TRAC project'
    print
    print 'sudo python backup_project.py -a'
    print 'in which case all available projects get backed up'


def backup_all():
    svn_projects = os.listdir(svn_home)

    header('Backing up Subversion/TRAC projects: %s' % time.asctime())
    for project in svn_projects:    
        backup(project)

def backup(project):
    
    dumppath = join(backup_dir, project)
    makedir(dumppath, cd=False)

    # Dump SVN repository
    projectpath = join(svn_home, project)
    dumpfile = join(dumppath, svndumpname)
    s = 'svnadmin dump %s > %s 2> %s' % (projectpath, dumpfile, errlog)
    err = run(s)
    if err != 0:
        print 'WARNING: SVN dump did not succeed for project %s. Error message was' % project        
        run('cat %s' % errlog, verbose=False)

    # Dump TRAC system
    projectpath = join(trac_home, project)
    dumpdir = join(dumppath, tracdumpname)
    
    run('/bin/rm -rf %s' % dumpdir, verbose=False) # Clean up in case there was one already

    s = 'trac-admin %s hotcopy %s > %s 2> %s' % (projectpath, dumpdir, logfile, errlog)
    err = run(s)
    if err != 0:
        print 'WARNING: TRAC hotcopy did not succeed for project %s. Error message was' % project        
        run('cat %s' % errlog, verbose=False)

    os.remove(errlog)
    os.remove(logfile)

if __name__ == '__main__':


    N = len(sys.argv)
    if not 2 <= N <= 2:
        usage()
        sys.exit()

    arg = sys.argv[1]

    # Make sure everything is clean
    consolidate_configuration_files()
    
    # Create backup dir
    makedir(backup_dir, cd=False)

    # Backup
    if arg == '-a':
        backup_all()
    else:
        backup(arg)
