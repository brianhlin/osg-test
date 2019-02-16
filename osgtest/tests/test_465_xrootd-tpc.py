import os
import socket
import shutil
import tempfile
import pwd
import requests

import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.osgunittest as osgunittest


class TestXrootdTPC(osgunittest.OSGTestCase):


    def test_01_create_macaroons(self):
        core.skip_ok_unless_installed('xrootd', 'xrootd-scitokens', by_dependency=True)
        euid = os.geteuid()
        cert = '/tmp/x509up_u%d' % euid
        key = '/tmp/x509up_u%d' % euid
        cert = os.environ.get('X509_USER_PROXY', cert)
        key = os.environ.get('X509_USER_PROXY', key)
 
        session = requests.Session()
        session.verify = False
        data_json = {"caveats": "activity:%s" % "DOWNLOAD",
                 "validity": 20}
        urlServer1 = ("http://",core.gethostname(),":9001", '/tmp/tmp.txt')
        response = session.post(urlServer1, 
                                headers={"Content-Type": "application/macaroon-request"},
                                data=json.dumps(data_json)
                               )
        
    
