# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.9.7)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x01\x58\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x10\x00\x00\x00\x10\x08\x04\x00\x00\x00\xb5\xfa\x37\xea\
\x00\x00\x00\x02\x73\x42\x49\x54\x08\x08\x55\xec\x46\x04\x00\x00\
\x00\x09\x70\x48\x59\x73\x00\x00\x00\xfb\x00\x00\x00\xfb\x01\x62\
\x78\xc7\x08\x00\x00\x00\x19\x74\x45\x58\x74\x53\x6f\x66\x74\x77\
\x61\x72\x65\x00\x77\x77\x77\x2e\x69\x6e\x6b\x73\x63\x61\x70\x65\
\x2e\x6f\x72\x67\x9b\xee\x3c\x1a\x00\x00\x00\xd7\x49\x44\x41\x54\
\x28\x91\x7d\xd1\xbf\x2b\xc4\x01\x18\xc7\xf1\x97\x94\x94\x5c\x19\
\x74\x49\xba\x95\x55\xd9\xd4\x65\x39\xe9\x6b\x40\x59\xce\x62\x34\
\xf0\x3f\x5c\x59\x4c\x17\x62\x31\x5a\x4c\xac\xb2\xb1\xb0\xf9\x13\
\xd4\x89\x14\xa7\xcb\x0d\xb7\x3e\x16\xd7\x7d\xbf\xf7\x75\xd7\x33\
\x3c\xbf\xde\x3d\x9f\xa7\xe7\x11\x7a\x66\xc4\x68\x3a\x0f\xa1\xeb\
\xa6\x1c\x79\xd0\xd6\xf1\xe4\xd8\x4c\x1f\x20\xf1\xee\xca\xa6\x39\
\x45\x89\x0b\x4d\x3b\x29\x40\xc5\xb7\x8d\xcc\xd8\x15\x6f\xf6\xfe\
\x62\x05\x0d\xdb\x39\xe5\x25\x6d\x0b\x41\x89\x9a\x9b\x5c\x7b\x51\
\xc9\x89\x53\xbb\x9e\xb9\x55\xcd\x01\x07\x5a\xce\x34\xb5\x94\xf9\
\x30\xdf\x0f\x04\x65\x2f\x42\x3d\x0c\x00\x82\x09\xfb\xc6\xc3\xbf\
\x12\x19\x50\xcd\xf5\x70\xa0\xa0\x61\x6b\x08\x10\x54\x7c\x49\x32\
\xc5\x65\x77\xc6\xd2\xa7\x5e\xf3\xea\xd2\xba\x59\xd3\x56\x9d\xfb\
\xec\xed\xd5\x75\x93\x0e\xdd\xfb\xd1\xf1\xa8\xae\x98\xfb\xe6\xe0\
\x77\xff\x02\x12\xa3\xce\x96\xee\x38\x9d\x9a\x00\x00\x00\x00\x49\
\x45\x4e\x44\xae\x42\x60\x82\
"

qt_resource_name = b"\
\x00\x07\
\x08\xbd\x8c\x78\
\x00\x72\
\x00\x65\x00\x66\x00\x72\x00\x65\x00\x73\x00\x68\
\x00\x0a\
\x05\x78\x4f\x27\
\x00\x72\
\x00\x65\x00\x6c\x00\x6f\x00\x61\x00\x64\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x14\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x14\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x7e\x75\xc4\xd9\x7f\
"

qt_version = QtCore.qVersion().split('.')
if qt_version < ['5', '8', '0']:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
