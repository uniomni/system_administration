"""Build clients in Beowulf cluster

This script will copy new installation to clients
"""

from config import nodes_to_build, client_image_dir, client_system_dirs
import os

print 'Creating client image dirs %s' % client_image_dir
try:
    os.mkdir(client_image_dir)
except OSError:
    pass

for hostname in nodes_to_build:
    os.chdir(client_image_dir)

    print 'Copying file system for %s' % hostname
    try:
        os.mkdir(hostname)
    except OSError:
        pass


    # Copy all system dirs to client area
    for dir in client_system_dirs:
        s = 'cp -aux /%s/. %s 2>/dev/null' % (dir, hostname)
        print s
        os.system(s)


    # Update boot area with same kernel used on head node
    boot_items = ['/boot', '/vmlinuz', '/initrd.img']
    for item in boot_items:
        cmd = 'rsync -rlHpWt %s %s/%s' % (item, client_image_dir, hostname)
        print cmd
        os.system(cmd)


