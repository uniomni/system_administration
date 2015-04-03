"""List file entries at specified URL

This is used specifically to get list of shakemaps uploaded to BNPB
"""

import os
import time
import urllib2

url = 'ftp://geospasial.bnpb.go.id'
shakestats = '/data_area/AIFDR_stats/shakemaps_uploaded_to_bnpb.csv'

def read_contents(url):
    """Read contents of url

       Return contents as a list
    """

    print 'Opening %s' % url
    fid = urllib2.urlopen(url)

    print 'Reading %s' % url
    entries = []
    for line in fid.readlines():
        fields = line.strip().split()
        if fields[-1].endswith('out.zip'):
            entries.append([fields[0], fields[-1]]) # Date and name
    return entries

if __name__ == '__main__':
    x = read_contents(url)

    # Organise by month
    stats = {}
    for entry in x:
        date = entry[0].split('-')
        month = date[0]
        year = date[-1]

        key = (year, month)
        if not stats.has_key(key):
            stats[key] = []

        stats[key].append(entry)


    # Output
    fid = open(shakestats, 'w')
    fid.write('Shakemaps uploaded to BNPB - updated %s\n\n' % time.asctime())
    fid.write('Year, Month, Count\n')
    for key in stats:
        fid.write('%s, %s, %s\n' % (key[0], key[1], len(stats[key])))


    fid.write('\n\n')
    fid.write('All entries by month\n')
    for entry in x:
        fid.write('%s, %s\n' % (entry[0], entry[1]))

    fid.close()


