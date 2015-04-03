"""This module provides functionality to load PostGIS with ESRI shapefiles

It relies on the underlying functionality of shp2pgsql and psql.
The script should be run as root.

Usage:
  python load_shapefiles.py <shapefiles> <database>
  
where <shapefiles> can be either a shapefile basename or a directory containing shapefiles. The latter form will recursively load all shapefiles encountered.  

It is assumed that associated files (shx, prj, ...) are available.
""" 

from utilities import run, replace_string_in_file, run_as_postgres, assign_owner
from config import logfile, errfile
import os, sys

hostname = 'localhost'
username = 'gis'
sql_files_generated = {}

def usage():
    print 'Usage:'
    print 'python load_shapefiles.py <shapefiles> <database>'

    
    
def create_sql_loader(shape_filename):
    """Convert shapefile and associated files into an sql loader
    """
    
    options = '-i' # Coerce integers to 32-bit. Needed by Arcview
    #options += '-s SRID'
    
    # Derive table name from shape filename
    path, name = os.path.split(shape_filename)
    basename, ext = os.path.splitext(name)

    table = basename
    sql_filename = table + '.sql'
    error_filename = table + '.err'
    
    s = 'shp2pgsql %s %s %s > %s 2>%s' % (options, 
                                          shape_filename, 
                                          table, 
                                          sql_filename,
                                          error_filename)
                                     
    #print s
    err = run(s)
    if err == 0:
        sql_files_generated[sql_filename] = None    
    else:
        print 'WARNING: Could not convert shapefile %s' % shape_filename
        print 'See error log %s' % error_filename

        
    # Patch sql file: ESRI cannot understand type numeric althoug QGIS can
    # Both will understand float, though.
    
    replace_string_in_file(sql_filename, 'numeric', 'float')
    
            
                
def create_sql_loaders(shpdir):
    """Recursively convert all shapefiles into sql loaders.
    """

    curdir = os.getcwd()
    
    if os.path.isfile(shpdir):   
        if shpdir.endswith('.shp'):
            create_sql_loader(os.path.join(curdir, shpdir))        
            return
        
        
    if os.path.isdir(shpdir):
        
        for dirpath, dirnames, filenames in os.walk(shpdir,
                                                    onerror=None,
                                                    followlinks=True):

            if '.svn' in dirnames:
                dirs.remove('.svn') # Don't visit SVN directories
                
            for filename in filenames:
            
                filenamex = filename.replace(' ', '\ ')
                create_sql_loaders(os.path.join(dirpath, filenamex))
                
    
def load_database(dbname):
    """Load sql vector data into PostGIS database
    """
    
    # Check if tables are there already
    #s = 'psql -d %s -h %s -U %s -c "\d"' % (dbname,     
    #                                        hostname,
    #                                        username)
    s = 'psql -d %s -c "\d"' % (dbname)     
    print s
    run_as_postgres(s)
    
    fid = open(logfile)
    tables = {}
    header_data = True
    for line in fid.readlines():
        fields = line.strip().split()
        if len(fields) == 0: continue 
        
        if not header_data:
            if len(fields) == 7:
                type = fields[4]
                
                if type == 'table':
                    tablename = fields[2]
                    tables[tablename] = 1
        
        if fields[0].startswith('----'):
            header_data = False

    
    print 
    print '--------------------------'
    print 'Tables already in database'
    print '--------------------------'    
    for table in tables:
        print table
    print
        

    print
    print '--------------------'
    print 'Loading into PostGIS'
    print '--------------------'                        
    for sqlfile in sql_files_generated.keys():
    
        s = 'Loading %s' % sqlfile
        print '-'*len(s)
        print s
        print '-'*len(s)        
        
        # First check that sql table isn't already in the database.
        tablename, _ = os.path.splitext(sqlfile)
        if tablename.lower() in tables:
            msg = 'WARNING: Table %s is already in database. ' % tablename
            msg += 'Consider renaming or delete'
            print msg
            print
            continue
    
        # Then attempt to load it
        basename, _ = os.path.splitext(sqlfile)
        #logfile = basename + '.log'
        #errfile = basename + '.err'        
        #s = 'psql -d %s -h %s -U %s -f %s > %s 2> %s' % (dbname, 
        #                                                 hostname,
        #                                                 username, 
        #                                                 sqlfile,
        #                                                 logfile,
        #                                                 errfile)
        
        s = 'psql -d %s -f %s' % (dbname, sqlfile) 
        print s        
        err = run_as_postgres(s)    
        
        fid = open(errfile)
        if len(fid.readlines()) > 2:
            err = 9999
        fid.close()
        
        if err != 0:
            print 'WARNING: Could not loadfile %s' % sqlfile
            print 'See error log %s' % errfile        
        print
        
        # Update permissions
        assign_owner(dbname, tablename, 'gis')                                
        
        
if __name__ == '__main__':

    N = len(sys.argv)
    if not 3 <= N <= 3:
        usage()
        sys.exit()
        
    shpdir = sys.argv[1]        
    dbname = sys.argv[2]

    
    print
    print '-------------------'
    print 'Create SQL loaders:'
    print '-------------------'        
    create_sql_loaders(shpdir)
    
    print
    print '--------------------'
    print 'Converted SQL files:'
    print '--------------------'    
    for name in sql_files_generated:
        print name
        
        
    print
    print '---------------------'
    print 'Connecting to PostGIS'
    print '---------------------'            
    load_database(dbname)
    
    
