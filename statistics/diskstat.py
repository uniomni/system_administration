"""Find old and large files on specified file system

Crosstabulate and organise by user.
This is useful to find files that are candidates for archiving.


Usage:

python diskstat.py <directory>

Example:

python diskstat.py d/cit/7



will generate things like

find . -xdev -type f -atime +365 -exec ls -la {} \; | gawk '{printf("%s %s %s\n", $3x, $5, $9)}'  | sort -k 1,1 -k2,2nr

"""

import os, time, sys


# Constants
days = 180 #365
filesize = 1000000  # One megabyte



# Useful Unix commands
ls_cmd = '-exec ls -la {} \\;'
filter_cmd = 'gawk \'{printf("%s %s %s\\n", $3x, $5, $8)}\' '
sort_cmd = 'sort -k 1,1 -k2,2nr ' # Sort on name and reversely by size


def make_filename(s):
    """Transform argument string into a suitable filename
    """

    s = s.strip()
    s = s.replace(' ', '_')
    #s = s.replace('(', '{')
    #s = s.replace(')', '}')
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace('__', '_')
    s = s.replace('/', '_')                    
        
    return s


def diskstat(findcommand, outfile, headline):

    import time

    tempfile = '/tmp/diskreport_' + str(time.time())

    # Find files
    cmd = findcommand
    cmd += ls_cmd + ' | ' + filter_cmd + ' | ' + sort_cmd
    cmd += ' > %s 2>/dev/null' % tempfile #Redirect
    print cmd
    os.system(cmd)

    # sort_and_clean(tempfile)

    # Organise them by name (with totals)
    fid = open(tempfile)
    lines = fid.readlines()
    fid.close()

    D = {}
    for line in lines:
        fields = line.strip().split()

        username = fields[0]
        size = long(fields[1])
        filename = fields[2]
        if not D.has_key(username):
            D[username] = []
        D[username].append( [filename, size] )

    # Find totals per user
    grand_total = 0
    totals = {}
    for username in D:
        total = 0
        for filename, size in D[username]:
            total += size

        totals[username] = total
        grand_total += total


    # Sort users by diskusage
    S = [(totals[username], username) for username in totals] #List comprehension    
    S.sort()
    S.reverse()
    users = [x[1] for x in S] #Users by diskusage


    # Write final result to disk
    fid = open(outfile, 'w')

    print
    txt = headline
    txt += '(%.3f MB):' %(grand_total/1.0e6)
    fid.write(txt + '\n')
    print '--------------------------------------------------'
    print txt
    print '--------------------------------------------------'    
    

    fid.write('\n')
    for username in users:
        fid.write('------------------------------------------------------\n')
        txt = '%s (%.3f MB)' %(username, totals[username]/1.0e6)
        fid.write(txt + '\n')
        fid.write('------------------------------------------------------\n')
        print txt

        for filename, size in D[username]:
            fid.write('    %s (%.3f MB)\n' %(filename, size/1.0e6))
        fid.write('\n')    


    fid.close()



if __name__ == '__main__':
    

    if len(sys.argv) > 1:
        dir = sys.argv[1]
    else:   
        dir = '.'
    

    # Check if gawk is installed
    if os.system('gawk --version >/dev/null') != 0:
        msg = 'Command gawk was not found, try\n'
        msg += 'sudo apt-get install gawk'
        raise Exception(msg)
    
    print 'DISKREPORT FOR DIRECTORY %s' %dir

    # Find the largest directories
    topname = 'top50_%s.txt' %(make_filename(dir))
    txt = 'Top 50 largest directories on %s (stated in kilo bytes)' %dir
    os.system('echo "%s" > %s' %(txt, topname))

    # Divide into two (had problems with broken pipe)
    cmd = 'du -k "%s" | sort -nr | head -50 >> %s' %(dir, topname)
    os.system(cmd)
    #cmd = 'du -k "%s" | sort -nr >> %s' %(dir, topname)
    #os.system(cmd)
    #cmd = 'cat %s | head -50 > %s' %(topname, topname)
    #os.system(cmd)



    #---------------
    # Find old files
    #---------------
    diskstat('find %s -xdev -type f -atime +%d ' %(dir, days),
             'oldfiles_%s.txt' %make_filename(dir),
             'Statistics for files on disk %s that haven\'t been accessed for at least %d days '\
             %(dir, days))


    #---------------
    # Find all files
    #---------------
    diskstat('find %s -xdev -type f ' %(dir),
             'allfiles_%s.txt' %make_filename(dir),         
             'Statistics for all files on disk %s '\
             %(dir))



    import sys; sys.exit()          
    #-----------------
    # Find large files
    #-----------------
    diskstat('find %s -xdev -type f -size +%dc ' %(dir, filesize),
             'bigfiles_%s.txt' %make_filename(dir),         
             'Statistics for files on disk %s that are larger than %.3f MB '\
             %(dir, filesize/1.0e6))


    #-------------------------
    # Find old and large files
    #-------------------------
    diskstat('find %s -xdev -type f -atime +%d -size +%dc '\
             %(dir, days, filesize),
             'oldbigfiles_%s.txt' %make_filename(dir),
             'Statistics for files on disk %s that haven\'t been accessed for at least %d days and that are larger than %.3f kB '\
             %(dir, days, filesize/1.0e6))

         


