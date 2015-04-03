This is a collection of Python scripts and text files that document the
installation of PostGIS and related spatial tools.

They are developed for use with the 
Australia-Indonesia Facility for Disaster Reduction (AIFDR) in Jakarta and
are aimed at the Ubuntu Jaunty operating environment but they
may be useful to a broader audience. 

The scripts do not automate everyhing - one must for example still manually add users to projects using trac-admin, but they do automate and document most of the configuration required.

The scripts are written in Python and must be run as root or using sudo.

The operations available are:


install_postgis_database.py:
	This script will download and configure the necessary
	Ubuntu/Debian packages necessary for setting up PostGIS

	
create_postgis_database.py <database>
	This script will create a new PostGIS database. 
	
config.py
	This file hosts a number of configurable parameters such
	as locations of files etc.			 
	
		

Further admin can be done by editing these files and through the
postgres user through the psql tool.



