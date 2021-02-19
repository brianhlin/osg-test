#!/usr/bin/python3

import os
import sys

sys.path.append(os.path.abspath('vm-test-runs/bin/'))

from vmu import PackageSet
from generate_dag import write_osg_test_configuration

SOURCES = sys.argv[1]
IS_NIGHTLY = sys.argv[4] == 'schedule'

PACKAGES = PackageSet(sys.argv[2],
                      sys.argv[3].split(','))


write_osg_test_configuration('docker',
                             ('',  # normally the test serial number
                              f'{SOURCES}',
                              PACKAGES),
                             '/tmp',
                             IS_NIGHTLY)
