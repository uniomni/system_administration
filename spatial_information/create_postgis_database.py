"""This script will install PostGIS

Should be run as root.
"""

from utilities import run, makedir, run_sqlcmd, run_as_postgres, assign_owner
import sys, os

def usage():
    print 'Usage:'
    #print 'sudo python create_postgis_database.py <project> [<administrator>]'
    print 'sudo python create_postgis_database.py <project>'

                       
def create_postgis_database(dbname):
    """Create new database with PostGIS functionality
    
    This can also be used as a template for other databases.
    E.g.
    
    createdb -T <template> -O <owner> <database name>
    
    where <template> is a database created by e.g. this function
    <database name> is just that; and
    <owner> could be created within psql as follows
    
    aifdr=# CREATE ROLE gisgroup NOSUPERUSER NOINHERIT CREATEDB NOCREATEROLE;
    CREATE ROLE
    aifdr=# CREATE ROLE gis LOGIN PASSWORD 'oialc' NOINHERIT;
    CREATE ROLE
    aifdr=# GRANT gisgroup TO gis;
    GRANT ROLE
    aifdr=# 

    aifdr=# ALTER TABLE geometry_columns OWNER TO gis;
    ALTER TABLE
    aifdr=# ALTER TABLE spatial_ref_sys OWNER TO gis;
    ALTER TABLE
    aifdr=# CREATE SCHEMA gis_schema AUTHORIZATION gis;
    CREATE SCHEMA
    aifdr=# 

    """
    
    s = 'createdb %s' % dbname     
    err = run_as_postgres(s)
    if err != 0:
        msg = 'Database %s already exists. ' % dbname
        msg += 'You can use dropdb to delete it as user posgres'
        # raise Exception(msg)
        print msg
        return
    
    
    s = 'createlang -d%s plpgsql' % dbname; run_as_postgres(s)
    s = 'psql -d%s -f /usr/share/postgresql/8.4/contrib/postgis.sql' % dbname; run_as_postgres(s)
    s = 'psql -d%s -f /usr/share/postgresql/8.4/contrib/spatial_ref_sys.sql' % dbname; run_as_postgres(s)

    
         
def test_installation(dbname):
    """Test that data base has been established 
    and print version number.
    """
    cmd = 'select postgis_lib_version();'    
    run_sqlcmd(dbname, cmd)
    os.system('cat sql.log')
    
    
if __name__ == '__main__':

    N = len(sys.argv)
    if not 2 <= N <= 2:
        usage()
        sys.exit()
        
    dbname = sys.argv[1]

    create_postgis_database(dbname)
    assign_owner(dbname, 'geometry_columns', 'gis')                            
    assign_owner(dbname, 'spatial_ref_sys', 'gis')                                
    test_installation(dbname)
