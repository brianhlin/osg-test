import os
import pwd
import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.service as service
import osgtest.library.osgunittest as osgunittest

XROOTD_CFG_TEXT = """\
cms.space min 2g 5g
xrootd.seclib /usr/lib64/libXrdSec.so
sec.protocol /usr/lib64 gsi -certdir:/etc/grid-security/certificates -cert:/etc/grid-security/xrd/xrdcert.pem -key:/etc/grid-security/xrd/xrdkey.pem -crl:3 -gridmap:/etc/grid-security/xrd/xrdmapfile --gmapopt:10 --gmapto:0
acc.authdb /etc/xrootd/auth_file
ofs.authorize
"""

AUTHFILE_TEXT = """\
u * /tmp a
u = /tmp/@=/ a
u xrootd /tmp a
"""

class TestStartXrootd(osgunittest.OSGTestCase):

    def test_01_config_auth(self):
        if core.osg_release() < 3.4:
            return

        core.skip_ok_unless_installed('xrootd', 'lcmaps-plugins-voms', 'xrootd-lcmaps', by_dependency=True)

        if core.el_release() > 6:
            core.config['xrootd.env'] = '/etc/systemd/system/xrootd.d/osg-test.conf'
            os.makedirs(os.path.dirname(core.config['xrootd.env']))
            files.write(core.config['xrootd.env'],
                        "[Service]\nEnvironment=\"LLGT_VOMS_ENABLE_CREDENTIAL_CHECK=1\"",
                        owner='xrootd')
        else:
            core.config['xrootd.env'] = '/etc/sysconfig/xrootd'
            files.append(core.config['xrootd.env'],
                         '''export LLGT_VOMS_ENABLE_CREDENTIAL_CHECK=1
export LCMAPS_DEBUG_LEVEL=5''',
                         owner='xrootd')

    def test_02_configure_xrootd(self):
        core.config['xrootd.pid-file'] = '/var/run/xrootd/xrootd-default.pid'
        core.config['certs.xrootdcert'] = '/etc/grid-security/xrd/xrdcert.pem'
        core.config['certs.xrootdkey'] = '/etc/grid-security/xrd/xrdkey.pem'
        core.config['xrootd.gsi'] = "ON"
        core.state['xrootd.started-server'] = False
        core.state['xrootd.backups-exist'] = False

        self.skip_ok_unless(core.options.adduser, 'user not created')
        vdt_pw = pwd.getpwnam(core.options.username)
        core.config['certs.usercert'] = os.path.join(vdt_pw.pw_dir, '.globus', 'usercert.pem')
        core.skip_ok_unless_installed('xrootd', by_dependency=True)

        user = pwd.getpwnam("xrootd")
        if core.config['xrootd.gsi'] == "ON":
            core.skip_ok_unless_installed('voms-clients-cpp')
            core.install_cert('certs.xrootdcert', 'certs.hostcert', 'xrootd', 0644)
            core.install_cert('certs.xrootdkey', 'certs.hostkey', 'xrootd', 0400)

            cfgfile = '/etc/xrootd/xrootd-clustered.cfg'
            files.append(cfgfile, XROOTD_CFG_TEXT, owner='xrootd', backup=True)
            authfile = '/etc/xrootd/auth_file'
            files.write(authfile, AUTHFILE_TEXT, owner="xrootd", chown=(user.pw_uid, user.pw_gid))

            files.write("/etc/grid-security/xrd/xrdmapfile", "\"%s\" vdttest" % core.config['user.cert_subject'],
                        owner="xrootd",
                        chown=(user.pw_uid, user.pw_gid))
            core.state['xrootd.backups-exist'] = True

    def test_03_configure_hdfs(self):
        core.skip_ok_unless_installed('xrootd-hdfs')
        cfgfile = '/etc/xrootd/xrootd-clustered.cfg'
        XROOTD_HDFS_CONFIG = "ofs.osslib /usr/lib64/libXrdHdfs.so"
        files.append(cfgfile, XROOTD_HDFS_CONFIG, backup=False)
        
    def test_04_start_xrootd(self):
        core.skip_ok_unless_installed('xrootd', by_dependency=True)
        if core.el_release() < 7:
            core.config['xrootd_service'] = "xrootd"
        else:
            core.config['xrootd_service'] = "xrootd@clustered"

        service.check_start(core.config['xrootd_service'])
        core.state['xrootd.started-server'] = True
