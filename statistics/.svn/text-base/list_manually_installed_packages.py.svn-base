"""List manually installed debian packages

Use as root or with sudo:
python list_manually_installed_packages.py [date]

output results to /var/log/manually_installed_software_<hostname>.csv

Optional argument [date] will list only packages installed since that date.
The date format is YYYYMMDD and be used e.g. as

python list_manually_installed_packages.py 20100201
python list_manually_installed_packages.py `date --date='last month' +'%Y%m%d'`


This script can be used in a crontab to list software installed every month. E.g.
# Make monthly list of manually installed software
# Note that the % character is interpreted by crontab as newline so it must be escaped as \%
1 1 1 * * root python /etc/system_administration/statistics/list_manually_installed_packages.py `date --date='last month' +'\%Y\%m\%d'` > /var/log/list_packages.log 2>&1


This was based on
http://superuser.com/questions/48374/ubuntu-find-out-all-user-installed-packages


REQUIRES
apt-get install aptitude

"""


import os, sys
from time import strftime, strptime, mktime, ctime, localtime, time as gettime
from subprocess import Popen, PIPE

tmpdir = '/tmp/dpkg_logfiles' # This must be a transient directory
logdir = '/var/log'
initial_status = '/var/log/installer/initial-status.gz'

hostname = os.uname()[1]
output_file = '/var/log/manually_installed_software_%s' % hostname


def get_all_packages():
    """Get all installed packages

    Name, version and their timestamp are returned in chronological order.

    Duplicates are removed using the latest entry.
    """

    os.system('/bin/rm -rf %s' % tmpdir)
    os.system('mkdir %s' % tmpdir)

    # Get copies of all log files
    files = os.listdir(logdir)
    for file in files:
        if file.startswith('dpkg.log'):
            os.system('cp -p %s %s' % (os.path.join(logdir, file), tmpdir))

    # Unzip if necessary
    files = os.listdir(tmpdir)
    for file in files:
        if not file.startswith('dpkg.log'):
            raise Exception()

        if file.endswith('.gz'):
            os.system('gunzip %s' % os.path.join(tmpdir, file))

    # Read log files and list unique packages
    packages = {}
    files = os.listdir(tmpdir)
    for file in files:
        fid = open(os.path.join(tmpdir, file))
        for line in fid.readlines():
            fields = line.strip().split()
            if fields[2] == 'install':
                date = fields[0]
                time = fields[1]
                name = fields[3]
                version = fields[5]

                # Convert time to seconds
                t = mktime(strptime(date + ' ' + time,
                                    '%Y-%m-%d %H:%M:%S'))
                entry = [t, date, time, name, version]
                packages[name] = entry
                #print name, version, date, time, t

    # Convert to list
    packages = packages.values()

    # Sort by time
    packages.sort()

    # Check
    t0 = 0
    for package in packages:
        assert package[0] >= t0
        t0 = package[0]

    return packages


def get_manually_installed_packages(date=None):
    """Get list of manually installed packages
    """

    all_packages = get_all_packages()

    if date is None:
        # Get time of fresh install
        t0 = os.path.getctime(initial_status)
        #print ctime(t0)
    else:
        # Use supplied date as starting point
        t0 = float(date)

    start_date = strftime('%Y%m%d', localtime(t0))
    end_date = strftime('%Y%m%d', localtime(gettime()))

    # Remove packages prior to initial system status
    new_packages = []
    for package in all_packages:
        if package[0] > t0:
            new_packages.append(package)

    # Remove t
    new_packages = [p[1:] for p in new_packages]

    # Remove automatically installed packages and add
    # detailed description to each entry
    packages = []
    for package in new_packages:
        date = package[0]
        time = package[1]
        name = package[2]
        cmd = 'aptitude show %s' % name
        p = Popen(cmd, shell=True,
                  stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

        # Extract Auto flag and description
        if p.stdout is not None:
            info = p.stdout.read().strip()
            lines = info.split('\n')
            auto = False
            description = 'None'
            for line in lines:
                fields = line.split(':')
                if fields[0].startswith('Automatically'):
                    auto = fields[1].lower().strip() == 'yes'
                if fields[0].startswith('Description'):
                    description = fields[1].replace(',', ' -')
            if not auto:
                package.append(description)
                packages.append(package)
                print '%s %s %s: %s' % (date, time, name, description)
        else:
            msg = 'Package %s had no description' % name
            raise Exception(msg)




    Nall = len(all_packages)
    Nnew = len(new_packages)
    Nman = len(packages)
    print('----------------------------')
    print('Total number of packages: %i' % Nall)
    print('Number of new packages: %i' % Nnew)
    print('Number of packages installed manually: %i' % Nman)
    print('')

    return packages, start_date, end_date


if __name__ == '__main__':

    N = len(sys.argv)
    if N > 1:
        date = sys.argv[1]
        msg = 'Date must have the format YYYYMMDD e.g. 20100214'
        assert len(date) == 8, msg

        # Convert date to seconds since epoch
        date = mktime(strptime(date, '%Y%m%d'))
    else:
        date = None


    packages, start_date, end_date = get_manually_installed_packages(date)

    output_file += '_%s_%s.csv' % (start_date, end_date)
    fid = open(output_file, 'w')
    fid.write('Date, Name, Version, Description\n')
    for p in packages:
        date = '%s %s' % (p[0], p[1])
        fid.write('%s, %s, %s, %s\n' % (date, p[2], p[3], p[4]))

    fid.close()
    print('List of manually installed software available in %s' % output_file)

