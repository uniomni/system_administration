"""Create Subversion project with TRAC support

Usage:

python create_project.py <project name>

It is assumed that all Subversion projects reside in 
/home/svn/<project name>
and that their associated TRAC pages are in
/home/trac/<project name>
This can be changed in config.py, though.

If project already exists, nothing is created and an error message is printed.


The Subversion repository can be checked out using
svn co --username <username> http://www.aifdr.org/svn/<project name>

The repository can be accessed from the web as URL
http://www.aifdr.org/svn/<project name>

And the TRAC pages are at
http://www.aifdr.org/projects/<project name>

See also create_user.py for creation of Subversion/TRAC user ids.

This script must be run as root or using sudo.
"""

import os, sys
from utilities import run, header, makedir, open_log, update_authentication_file, replace_string_in_file
from config import password_filename, auth_filename, trac_header, trac_home, svn_header, svn_home
from config import filenames_updated


def usage():
    print 'Usage:'
    print 'sudo python create_project.py <project> [<administrator>]'


def check_existence_of_project(project):
    """Check if Subversion or TRAC directory already exists
    """
    
    for x in [svn_home, trac_home]:
        try:
            dirs = os.listdir(x)
        except:
            continue # OK if svn or trac doesn't exist 

        
        for dir in dirs:
            if dir == project:
                msg = 'Project %s already exists in %s\n' % (project, x)
                msg += 'Try another name or delete existing directory' 
                raise Exception(msg)
            
    
def create_subversion_repository(project):
    """Create and configure Subversion
    """
    header('Creating Subversion configuration for %s' % project)    

    # Create svn home dir if it doesn't exist and change to it
    makedir(svn_home)
        
    # Create repository 
    project_dir = os.path.join(svn_home, project)
    s = 'svnadmin create %s' % project_dir
    run(s)
    
    s = 'chown -R www-data:www-data %s' % project_dir
    run(s)
    
    s = 'chmod -R 755 %s' % project_dir
    run(s)    
    
    
    # Add information to the Apache web server
    fid = open_log('/etc/apache2/mods-enabled/dav_svn.conf', 'a')
    fid.write('\n%s%s\n' % (svn_header, project))
    fid.write('<Location /svn/%s>\n' % project)
    fid.write('  DAV svn\n')
    fid.write('  SVNPath %s\n' % project_dir)
    fid.write('  AuthType Basic\n')
    fid.write('  AuthName "Subversion Repository"\n')
    fid.write('  AuthUserFile %s\n' % password_filename) 
    fid.write('  AuthzSVNAccessFile %s\n' % auth_filename)
    fid.write('  Require valid-user\n')
    fid.write('</Location>\n')
    fid.close()

    # Make sure authentication file is available
    # FIXME (Ole): Groups are hardwired for now
    if not os.path.isfile(auth_filename):
        fid = open_log(auth_filename, 'w')
        fid.write('[groups]\n')
        fid.write('aifdr =\n')
        fid.write('guests =\n')
        fid.close()
         
    # Add project to authorization file
    fid = open_log(auth_filename, 'a')
    fid.write('\n')
    fid.write('[%s:/]\n' % project)
    fid.write('@aifdr = rw\n')
    fid.write('@guests = r\n')
    fid.close()    
    
def get_TRAC_version():
    fid = os.popen('trac-admin')
    line = fid.readline()
    fid.close()

    assert line.startswith('trac-admin')
    fields = line.split()

    version = fields[-1] 
    print 'Got TRAC version: ', version
    return version
    
def create_trac_environment(project, administrator=None):
    """Create and configure TRAC
    """
    header('Creating TRAC configuration for %s' % project)        

    # Create trac home dir if it doesn't exist
    makedir(trac_home)

    project_home = os.path.join(trac_home, project)
    # Create environment 
    s = 'trac-admin %s initenv ' % project_home
    s += '%s ' % project  # Project name
    s += '%s ' % 'sqlite:db/trac.db' # Database connection string
    s += '%s ' % 'svn'    # Repository type
    s += '%s ' % os.path.join(svn_home, project) # Path to repository

    # Temporary fix to reflect changes from TRAC 0.10.4 to 0.11.1
    v = get_TRAC_version()
    if v not in ['0.11.1', '0.11.4']:
        # Templates directory (Only in TRAC 0.10.4, gone in 0.11.1)
        s += '/usr/share/trac/templates'

    s += ' > initenv.log'
    s += ' 2> initenv.err'
    err=run(s)    
    if err != 0:
        msg = 'TRAC initenv failed to complete. See initenv.log and initenv.err for details'
        raise Exception(msg)
    # Clean up log files
    os.remove('initenv.log')
    os.remove('initenv.err')
    
    s = 'chown -R www-data:www-data %s' % project_home
    run(s)
    
    s = 'chmod -R 755 %s' % project_home
    run(s)        
    
    # Add information to the Apache web server
    fid = open_log('/etc/apache2/httpd.conf', 'a')
    fid.write('\n%s%s\n' % (trac_header, project))
    fid.write('<Location /projects/%s>\n' % project)
    fid.write('   SetHandler mod_python\n')
    fid.write('   PythonInterpreter main_interpreter\n')
    fid.write('   PythonHandler trac.web.modpython_frontend\n') 
    fid.write('   PythonOption TracEnv %s\n' % project_home)
    fid.write('   PythonOption TracUriRoot /projects/%s\n' % project)
    #fid.write('   PythonDebug on\n')
    fid.write('</Location>\n\n')
    
    fid.write('<Location /projects/%s/login>\n' % project)
    fid.write('   AuthType Basic\n')
    fid.write('   AuthName "%s"\n' % project)
    fid.write('   AuthUserFile %s\n' % password_filename)
    fid.write('   Require valid-user\n')
    fid.write('</Location>\n')
    
    fid.close()

    # Set default TRAC permissions
    os.chdir('%s' % project_home)
    s = "trac-admin . permission remove '*' '*'"
    run(s)
    #s = "trac-admin . permission add anonymous WIKI_VIEW"
    #run(s)
    #s = "trac-admin . permission add authenticated WIKI_ADMIN"
    #run(s)
    #s = "trac-admin . permission add authenticated TICKET_ADMIN"    
    #run(s)
    s = "trac-admin . permission add authenticated WIKI_VIEW"
    run(s)
    

    if administrator is not None:
        s = "trac-admin . permission add %s TRAC_ADMIN" % administrator   
        run(s)        

    # Patch trac-ini to avoid annoying 'missing header_logo'
    filename = os.path.join(project_home, 'conf', 'trac.ini')
    
    replace_string_in_file(filename, 
                           'alt = (please configure the [header_logo] section in trac.ini)',
                           'alt = ')
    replace_string_in_file(filename, 
                           'src = site/your_project_logo.png',
                           'src =')

                           
    
if __name__ == '__main__':
    N = len(sys.argv)
    if not 2 <= N <= 3:
        usage()
        sys.exit()
        

    project = sys.argv[1]
    if N == 3:
        administrator = sys.argv[2]

        # Check if this user exists
        fid = open(password_filename)
        user_exists = False
        for line in fid.readlines():
            if line.startswith(administrator): 
                user_exists = True
                break
        fid.close()
        
        if user_exists:
            # Make sure user is authenticated
            update_authentication_file(administrator)
        else:
            print 'Requested administrator %s does not exist as Subversion/TRAC user' % administrator
            print 'Please run the script: create_user.py %s first' % administrator 
            import sys; sys.exit()
    else: 
        administrator = None


    check_existence_of_project(project)        
    create_subversion_repository(project)
    create_trac_environment(project, administrator)    
    
    # Restart web server
    run('/etc/init.d/apache2 restart')

    print
    header('Repository %s created.' % project)
    print 'The Subversion URL is http://<web server>/svn/%s' % project
    print 'The TRAC pages are available at http://<web server>/projects/%s' % project
    print
    print 'Files modified:'
    print filenames_updated.keys()
    print 
    print 'Possibly modify file %s for access details' % auth_filename
    #os.system('cat %s' % auth_filename)    
    
