
auth_filename = '/etc/apache2/dav_svn.authz'
password_filename = '/etc/apache2/dav_svn.passwd'
filenames_updated = {} # Keep track of files edited
trac_header = '# TRAC pages for project: ' # Must have a colon as used to split
svn_header = '# Subversion repository for project: ' # Must have a colon as used to split
trac_home = '/home/trac'
svn_home = '/home/svn'

# Backup stuff
backup_dir = '/home/repository_backup'
svndumpname = 'svn.dump'
tracdumpname = 'trac.dump'

# Logging
errlog = 'errorlog.txt'
logfile = 'log.txt'
