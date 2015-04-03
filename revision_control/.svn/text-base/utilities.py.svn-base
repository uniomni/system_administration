"""Utilities used with administration of revision control and TRAC
"""
import os
from config import filenames_updated, auth_filename, trac_header, trac_home, svn_header, svn_home
            
def run(s, verbose=True):
    if verbose:
        print s

    err = os.system(s)
    return err
    
def header(s):
    dashes = '-'*len(s)
    print
    print dashes
    print s
    print dashes
    
def open_log(s, mode='r'):
    """Open file as normally, but log those that are being written to
    It is assumed that this file gets cleared out by the script using 
    this function
    """

    fid = open(s, mode)
    
    if mode in ['w', 'a']:
        filenames_updated[s] = 1
    
    return fid

    
def makedir(newdir, cd=True):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
        - changes to newly created dir (if cd is True)

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
        if head and not os.path.isdir(head):
            makedir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)

    if cd:
        os.chdir(newdir)


def replace_string_in_file(filename, s1, s2):
    """Replace string s1 with string s2 in filename 
    """

    # Read data from filename
    infile = open(filename)
    lines = infile.readlines()
    infile.close()

    # Replace and store updated versions
    outfile = open(filename, 'w')
    for s in lines:
        new_string = s.replace(s1, s2).rstrip()

        if new_string.strip() != s.strip():
            print 'Replaced %s with %s' % (s, new_string)
        
        outfile.write(new_string + '\n')
    outfile.close()



def update_authentication_file(username):
    """Add new user to /etc/apache2/dav_svn.authz
    If user already exists, print warning and do nothing
    
    FIXME (Ole): For the time being, all new users are added to 
    the aifdr group.
    """
    
    # Make sure authentication file is available
    # FIXME (Ole): Groups are hardwired for now
    if not os.path.isfile(auth_filename):
        fid = open_log(auth_filename, 'w')
        fid.write('[groups]\n')
        fid.write('aifdr = \n')
        fid.write('guests =\n')
        fid.close()
    
    # Add this user to the aifdr group     
    fid = open_log(auth_filename)
    lines = fid.readlines()
    fid.close()
    
    fid = open_log(auth_filename, 'w')    
    for line in lines:
        if line.startswith('aifdr'):
            # Add user if not there already 
            if line.find(username) == -1:
                line = line.rstrip() + ',%s\n' % username
            else:
                s = 'User %s has already been recorded in %s. '\
                    % (username, auth_filename)
                print s 
    
        fid.write(line)
    fid.close()


def consolidate_configuration_files():
    """Remove deleted projects and users from configuration files
    """

    # Get list of repositories that have both svn and trac
    svn_projects = os.listdir(svn_home)
    trac_projects = os.listdir(trac_home)
    projects = []

    for project in svn_projects:
        if project in trac_projects:
            projects.append(project)
        else:
            print 'WARNING: %s has SVN support but not TRAC' % project

    for project in trac_projects:
        if project not in svn_projects:
            print 'WARNING: %s has TRAC support but not SVN' % project
            

    # Update configuration files so that only discovered projects have entries

    #-----------------------
    # httpd.conf
    #-----------------------
    httpd_conf = '/etc/apache2/httpd.conf'
    
    print 'Cleaning %s - backup made in %s-BACKUP' % (httpd_conf, httpd_conf)
    s = 'cp %s %s-BACKUP'  % (httpd_conf, httpd_conf)
    run(s, verbose=False)

    fid = open(httpd_conf)
    lines = fid.readlines()
    fid.close()
    
    fid = open(httpd_conf, 'w')
    keep = True
    for line in lines:
        if line.startswith(trac_header):
            project = line.split(':')[-1].strip()
            #print 'Found project', project
            
            if project in projects:
                keep = True
            else:
                print 'Project %s does not have SVN/TRAC support - deleting entry.' % project
                keep = False
                

        if keep:
            fid.write(line)
    fid.close()
    
            

    #-----------------------
    # dav_svn.conf
    #-----------------------
    dav_svn_conf = '/etc/apache2/mods-available/dav_svn.conf'

    print 'Cleaning %s - backup made in %s-BACKUP' % (dav_svn_conf, dav_svn_conf)
    s = 'cp %s %s-BACKUP'  % (dav_svn_conf, dav_svn_conf)
    run(s, verbose=False)

    fid = open(dav_svn_conf)
    lines = fid.readlines()
    fid.close()
    
    fid = open(dav_svn_conf, 'w')
    keep = True
    for line in lines:
        if line.startswith(svn_header):
            project = line.split(':')[-1].strip()
            #print 'Found project', project

            if project in projects:
                keep = True
            else:
                print 'Project %s does not have SVN/TRAC support - deleting entry.' % project
                keep = False
                

        if keep:
            fid.write(line)

    fid.close()

    
    #-----------------------
    # dav_svn.authz
    #-----------------------            

    print 'Cleaning %s - backup made in %s-BACKUP' % (auth_filename, auth_filename)
    s = 'cp %s %s-BACKUP'  % (auth_filename, auth_filename)
    run(s, verbose=False)

    fid = open(auth_filename)
    lines = fid.readlines()
    fid.close()
    
    fid = open(auth_filename, 'w')
    keep = False
    groups = True
    for i, line in enumerate(lines):
        # First process [groups] (must be the first entry)
        if line.startswith('[groups]'):
            keep = True
            groups = True
        elif groups:
            # FIXME: Check usernames
            pass
        
        if line.strip().endswith(':/]'):
            groups = False
            project = line.split(':')[0].strip()[1:]
            #print 'Found project', project

            if project in projects:
                keep = True
            else:
                print 'Project %s does not have SVN/TRAC support - deleting entry.' % project
                keep = False
                

        if keep:
            fid.write(line)

    fid.close()


    # Now create entries for orphaned projects i.e. projects in /home/svn and /home/trac
    #FIXME: TODO
