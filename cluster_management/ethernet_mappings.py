"""Ethernet mappings for compute nodes
"""

# COMPUTE NODES
# The alamba compute nodes maps ethernet cards to eth5 to eth8 to avoid clashes with what the node thinks is mapped to eth0-eth3.
# This is set in the (generated) file /etc/70-persistent-net.rules

# eth7 and eth8 are bonded into bond0 for access to the NAS storage


# COMPUTE NODES (The original mapping)
# The alamba compute nodes use the following mapping:
# eth0: port 1 on Mezzanine card
# eth1: NIC 1 on main board
# eth2: port 2 on Mezzanine card
# eth3: NIC 2 on main board
#
# HEAD NODE
# The head node uses a different mapping providing eth0 to eth7.
# eth0: NIC 1
# eth1: NIC 2
# eth2: NIC 3
# eth3: NIC 4
# eth4: NIC 5
# eth5: NIC 6
# eth6: NIC 7
# eth7: NIC 8
#
# eth0:
# eth1: Alamba net
# eth2: NAS
# eth3: NAS
# eth4: Internet connection
# eth5: Management (e.g. from AIFDR office)
# eth6:
# eth7:
#
# eth2 and eth3 are bonded into bond1 for access to the NAS storage.

# Map eth-interfaces for each node to mac-addresses
mac_addr = {'node1': {'eth0': '00-26-55-83-aa-58',
                      'eth5': '00-24-81-af-83-30',
                      'eth7': '00-24-81-af-83-32',
                      'eth8': '00-26-55-83-aa-5c'},
            'node2': {'eth0': '00-25-b3-a6-92-90',
                      'eth5': '00-24-81-af-54-1c',
                      'eth7': '00-24-81-af-54-1e',
                      'eth8': '00-25-b3-a6-92-94'},
            'node3': {'eth0': '00-26-55-84-da-78',
                      'eth5': '00-24-81-af-e3-00',
                      'eth7': '00-24-81-af-e3-02',
                      'eth8': '00-26-55-84-da-7c'},
            'node4': {'eth0': '00-25-b3-a8-b0-10',
                      'eth5': '00-24-81-af-e3-d4',
                      'eth7': '00-24-81-af-e3-d6',
                      'eth8': '00-25-b3-a8-b0-10'},
            'node5': {'eth0': '00-25-b3-a8-a1-e0',
                      'eth5': '00-24-81-af-93-ac',
                      'eth7': '00-24-81-af-93-ae',
                      'eth8': '00-25-b3-a8-a1-e4'},
            'node6': {'eth0': '00-25-b3-a7-9c-78',
                      'eth5': '00-24-81-af-b3-d0',
                      'eth7': '00-24-81-af-b3-d2',
                      'eth8': '00-25-b3-a7-9c-78'},
            'node7': {'eth0': '00-25-b3-a8-10-28',
                      'eth5': '00-24-81-af-14-ec',
                      'eth7': '00-24-81-af-14-ee',
                      'eth8': '00-25-b3-a8-10-2c'},
            'node8': {'eth0': '00-25-b3-a7-be-40',
                      'eth5': '00-24-81-af-93-20',
                      'eth7': '00-24-81-af-93-22',
                      'eth8': '00-25-b3-a7-be-44'},
            'node9': {'eth0': '00-25-b3-a8-30-48',
                      'eth5': '00-24-81-af-d3-1c',
                      'eth7': '00-24-81-af-d3-1e',
                      'eth8': '00-25-b3-a8-30-4c'},
            'node10': {'eth0': '00-25-b3-a7-d9-d8',
                       'eth5': '00-24-81-af-04-10',
                       'eth7': '00-24-81-af-04-12',
                       'eth8': '00-25-b3-a7-d9-dc'},
            'node11': {'eth0': '00-25-b3-a8-00-90',
                       'eth5': '00-24-81-af-d3-30',
                       'eth7': '00-24-81-af-d3-32',
                       'eth8': '00-25-b3-a8-00-94'},
            'node12': {'eth0': '00-25-b3-a7-7a-40',
                       'eth5': '00-24-81-af-34-d4',
                       'eth7': '00-24-81-af-34-d6',
                       'eth8': '00-25-b3-a7-7a-44'},
            'node13': {'eth0': '00-25-b3-a7-bd-40',
                       'eth5': '00-24-81-af-83-1c',
                       'eth7': '00-24-81-af-83-1e',
                       'eth8': '00-25-b3-a7-bd-44'},
            'node14': {'eth0': '00-25-b3-a8-60-78',
                       'eth5': '00-24-81-af-24-98',
                       'eth7': '00-24-81-af-24-9a',
                       'eth8': '00-25-b3-a8-60-7c'},
            'node15': {'eth0': '00-25-b3-a7-de-48',
                       'eth5': '00-24-81-af-c3-94',
                       'eth7': '00-24-81-af-c3-96',
                       'eth8': '00-25-b3-a7-de-4c'},
            'node16': {'eth0': '00-25-b3-a7-2e-30',
                       'eth5': '00-24-81-af-34-dc',
                       'eth7': '00-24-81-af-34-de',
                       'eth8': '00-25-b3-a7-2e-34'},
            'node17': {'eth0': '00-25-b3-a7-fc-e0',
                       'eth5': '00-24-81-af-e3-4c',
                       'eth7': '00-24-81-af-e3-4e',
                       'eth8': '00-25-b3-a7-fc-e4'},
            'node18': {'eth0': '00-25-b3-a7-ef-20',
                       'eth5': '00-24-81-af-c3-98',
                       'eth7': '00-24-81-af-c3-9a',
                       'eth8': '00-25-b3-a7-ef-24'},
            'node19': {'eth0': '00-25-b3-a7-0c-a8',
                       'eth5': '00-24-81-af-b3-9c',
                       'eth7': '00-24-81-af-b3-9e',
                       'eth8': '00-25-b3-a7-0c-ac'},
            'node20': {'eth0': '00-25-b3-a8-a1-b0',
                       'eth5': '00-24-81-af-e3-30',
                       'eth7': '00-24-81-af-e3-32',
                       'eth8': '00-25-b3-a8-a1-b4'}}


# Create alphabetically ordered list of ethernet cards
interface_names = mac_addr['node1'].keys()
interface_names.sort()
#interface_names = ['eth0', 'eth7', 'eth8']
