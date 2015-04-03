"""Utilities
  
"""  

import os        
from math import sqrt, pi, sin, cos, acos
from subprocess import Popen, PIPE
import sys

def run(cmd, 
        stdout=None,
        stderr=None, 
        verbose=True):
        
    s = cmd    
    if stdout:
        s += ' > %s' % stdout
        
    if stderr:
        s += ' 2> %s' % stderr        
        
    if verbose:
        print s
    err = os.system(s)
    
    if err != 0:
        msg = 'Command "%s" failed with errorcode %i. ' % (cmd, err)
        if stderr: msg += 'See logfile %s for details' % stderr
        raise Exception(msg)

    
def header(s):
    dashes = '-'*len(s)
    print
    print dashes
    print s
    print dashes
    
def write_line(fid, text, indent=0):
    fid.write(' '*indent + text + '\n')

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
        if head and not os.path.isdir(head):
            makedir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)

        
def get_username():
    """Get username
    """
    p = Popen('whoami', shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
              
    if p.stdout is not None:
        username = p.stdout.read().strip()
    else:
        username = 'unknown'
        
        
    #print 'Got username', username
    return username
    
def get_timestamp():
    """Get timestamp in the ISO 8601 format
    
    http://www.iso.org/iso/date_and_time_format
    
    Format YYYY-MM-DDThh:mm:ss
    where the capital letter T is used to separate the date and time 
    components. 
    
    Example: 2009-04-01T13:01:02 represents one minute and two seconds 
    after one o'clock in the afternoon on the first of April 2009. 
    """
    
    from time import strftime
    #return strftime('%Y-%m-%dT%H:%M:%S') # ISO 8601
    return strftime('%Y-%m-%dT%H%M%S') # Something Windows can read

    
def get_shell():
    """Get shell if UNIX platform
    Otherwise return None
    """
    
    p = Popen('echo $SHELL', shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
              
    shell = None
    if p.stdout is not None:
        shell = p.stdout.read().strip()
        shell = os.path.split(shell)[-1] # Only last part of path
        
    return shell

    
    

def replace_string_in_file(filename, s1, s2, verbose=False):
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

        if new_string.strip() != s.strip() and verbose:
            print 'Replaced %s with %s' % (s, new_string)
        
        outfile.write(new_string + '\n')
    outfile.close()

