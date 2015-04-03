This is a collection of Python scripts that document the
installation of Subversion repositories with TRAC support.

They are developed for use with the 
Australia-Indonesia Facility for Disaster Reduction (AIFDR) in Jakarta and
are aimed at the Ubuntu Jaunty operating environment but they
may be useful to a broader audience. 

The scripts do not automate everyhing - one must for example still manually add users to projects using trac-admin, but they do automate and document most of the configuration required.

The scripts are written in Python and must be run as root or using sudo.

The operations available are:


install_trac_and_subversion.py:
	This script will download and configure the necessary
	Ubuntu/Debian packages necessary for setting up 
	Subversion and TRAC
	
create_project.py <project> [<administrator>]
	This script will create a new Subversion repository 
	and TRAC site with name <project>. The optional argument
	<administrator> gives TRAC_ADMIN permissions to a the
	user name specified.
	
create_user.py <user>
	This script will create a new user to access Subversion
	and TRAC. The script will prompt for password.
	
remove_project.py <project>
	This script will cleanup all references to specified project.
	
config.py
	This file hosts a number of configurable parameters such
	as locations of files etc.			 
	
		

The files and directories modified by these scripts are		
/etc/apache2/dav_svn.authz 
/etc/apache2/dav_svn.passwd
/etc/apache2/mods-enabled/dav_svn.conf
/etc/apache2/httpd.conf
/home/trac
/home/svn

Further admin can be done by editing these files and through the
TRAC website. You can also run trac-admin and svnadmin as normally


