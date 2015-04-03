"""Load Subversion/TRAC project from backup

Usage 
    python load_project.py <project> [<target>]

Without optional argument target project will be loaded from backup into new project of the same name.
With target specified project will be loaded from backup into project named target.

<project> can either be the (directory) name of a project backed up by backup_project.py or an svn dump file. 

Example:
To try this procedure (say the project is called moonie), you can backup, delete, create and reload it follows
python backup_project.py moonie
python remove_project.py moonie
python create_project.py moonie
python load_project.py moonie


Notes:
* A new empty project must be created before loading it, e.g.
  python create_project.py <target>
* The group permissions in /etc/apache2/dav_svn.authz may need to be updated manually
"""

#FIXME: Allow -a option to load all, just like backup_project

from config import svn_home, trac_home, backup_dir, svndumpname, tracdumpname, errlog, logfile
from utilities import run
from os.path import join, isfile
import sys

def usage():
    print 'Usage:'
    print 'sudo python load_project.py <project> [<target>]'
    print 'where <project> is the name of a previously backed up project'
    print 'and <target> a new empty project.'
    print 'If <target> is omitted it is assumed that it has the same name as the backup'

    
if __name__ == '__main__':
    N = len(sys.argv)
    if not 2 <= N <= 3:
        usage()
        sys.exit()
        

    project = sys.argv[1]
    if N == 3:
        target = sys.argv[2]
    else: 
        target = project


    # Load Subversion repository
    dumppath = join(backup_dir, project)
    projectpath = join(svn_home, target)
    if isfile(dumppath):
        # User might have specified svn dump file explicitly
        dumpfile = dumppath
    else:    
        dumpfile = join(dumppath, svndumpname)

    s = 'svnadmin load %s < %s' % (projectpath, dumpfile)
    err = run(s, verbose=True)
    if err != 0:
        msg = 'SVN repository could not be loaded. This can forexample happen if empty target project does not exist\n'
        msg += 'Try to create a new target project using e.g. create_project.py'
        raise Exception(msg)

    # Load TRAC pages
    projectpath = join(trac_home, target)
    dumpdir = join(dumppath, tracdumpname)

    s = 'rsync -avz %s/* %s' % (dumpdir, projectpath)
    run(s)

    # Synchronise TRAC with repository
    s = 'trac-admin %s resync' % projectpath
    run(s)

    # Set ownership
    s = 'chown -R www-data:www-data %s' % projectpath
    run(s)

