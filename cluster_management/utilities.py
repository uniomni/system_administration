"""This script contains utilities used by other scripts
"""

import os, string

class NICinfo:
    """Represent one network card (NIC) in terms of
    mac address and ip address
    """
    def __init__(self, mac, ip):
        self.mac = mac
        self.ip =  ip

    def __repr__(self):
        s = 'ip = %s, ' % self.ip
        s += 'mac = %s' % self.mac

        return s

class Nodeinfo:
    """Represent two network cards (NICs):
    One for the PXE boot and one for the subsequent
    network communication
    """
    def __init__(self, pxe, net, nas):
        self.pxe = pxe
        self.net = net
        self.nas = nas

    def __repr__(self):
        s = '\n    PXE: %s\n' % self.pxe
        s += '    NET: %s\n' % self.net
        s += '    NAS: %s\n' % self.nas
        return s

def get_class_c_addr(ip):
    """Return first three segments of network address separated by dots
    """
    return string.join(ip.split('.')[:3], '.')

def reverse_addr(ip):
    """Reverse ip address separated by dots.
    """

    x = ip.split('.')
    x.reverse()
    return string.join(x, '.')

def add2addr(ip, i):
    """Add i to rightmost field of ip address

    If result exceeds 255 an exception is raised
    """

    x = ip.split('.')
    y = int(x[3]) + i
    x[3] = str(y)
    x = string.join(x, '.')
    if y > 255:
        msg = 'IP address %s is invalid' % x
        raise Exception(msg)

    return x

def get_kernel_name():
    """Get kernel name from server installation in /boot
    Looking for something like vmlinuz-2.6.28-11-generic
    This approach will take the first match as the kernel name
    """

    #print 'Searching for kernel in /boot'
    kernel_name = None
    for file in os.listdir('/boot'):
        if file.startswith('vmlinuz'):
            kernel_name = file
            break

    if not kernel_name:
        msg = ('Could not find kernel file '
               '(assume it is in /boot and starts with vmlinuz)')
        raise Exception(msg)
    else:
        print 'Found kernel_name: %s' % kernel_name
        return kernel_name

