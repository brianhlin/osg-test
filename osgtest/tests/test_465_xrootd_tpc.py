import os
import json
import requests

import osgtest.library.core as core
import osgtest.library.osgunittest as osgunittest


class TestXrootdTPC(osgunittest.OSGTestCase):

    __data_path = '/usr/share/osg-test/test_gridftp_data.txt'

    def test_01_create_macaroons(self):
        return True
