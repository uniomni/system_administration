"""
Load all projects back up
"""
from subprocess import call
project_list = ['CentroidPlugin',
                'distream',
                'earthquake_hazard_modelling',
                'geoserver_python',
                'gis',
                'impact_map',
                'inasafe_data',
                'index',
                'mentawai_TTX',
                'papua_eq_hazard',
                'seismologi_teknik',
                'sulawesi_eq_hazard',
                'sumatra_eq_hazard',
                'tephra',
                'tsunami',
                'tsutime',
                'volcanic_ash_modelling']
#'aim',
#'system_administration']
for project in project_list:
    # Create new project with existing name'
    cmd = 'sudo python /etc/system_administration/revision_control/create_project.py ' + project + ' griffij'
    print cmd
    call(cmd, shell=True)

    # Dump old data
    cmd = 'sudo svnadmin dump  --quiet /home/rangga/webserver/svn/%s > /home/griffij/%s.dump' % (project, project)
    print cmd
    call(cmd, shell=True)

    # Upload old data to new project
    cmd = 'sudo python /etc/system_administration/revision_control/load_project.py /home/griffij/%s.dump %s' % (project, project)
    print cmd
    call(cmd, shell=True)

    # Dump trac pages
    cmd = 'sudo trac-admin /home/rangga/webserver/trac/%s wiki dump /home/griffij/trac/%s' % (project, project)
    print cmd
    call(cmd, shell=True) 

    # Upload old trac pages
    cmd = 'sudo trac-admin /home/trac/%s/ wiki load /home/griffij/trac/%s/' % (project, project)
    print cmd
    call(cmd, shell=True)

