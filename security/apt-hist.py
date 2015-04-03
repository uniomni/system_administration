#!/usr/bin/env python

"""Program to show apt install history.

usage:  apt-hist
"""

# where the apt logfile is
LogFile = '/var/log/apt/history.log'

# date string, precedes '2011-02-04  10:21:02'
StartDate = 'Start-Date: '

# command string, precedes actual command
CommandLine = 'Commandline: '


def main():
    """Read the history file, printing install commands."""

    last_date = None

    with open(LogFile) as fp:
        lines = fp.readlines()

    len_date = len(StartDate)
    len_cmd = len(CommandLine)

    for line in lines:
        line = line.strip()
        if line.startswith(StartDate):
            last_date = line[len_date:len_date+11] + line[len_date+12:len_date+20]
        elif line.startswith(CommandLine):
            cmd = line[len_cmd:]
            print('%s: %s' % (last_date, cmd))


if __name__ == '__main__':
    import sys

    if len(sys.argv):
        print __doc__
        sys.exit(0)

    main()
