"""Find all directories containing shapefiles
"""
import sys, os

if len(sys.argv) > 1:
    rootdir = sys.argv[1]
else:
    rootdir = '.'

shapedirs = {}
for dirpath, dirnames, filenames in os.walk(rootdir):

    for filename in filenames:
        if filename.endswith('shp'):
            shapedirs[dirpath] = None
            #print dirpath
            #print filename


print
print 'Dirs with shapefiles:'
for dir in shapedirs.keys():

    dirx = dir.replace(' ', '\ ')
    dirx = dirx.replace('&', '\&')    
    s = 'du -sh %s' % dirx
    os.system(s)
    s = 'rsync -avz %s ole@nautilus:Kristy' % dirx
    print s
    os.system(s)
    #import sys; sys.exit() 
