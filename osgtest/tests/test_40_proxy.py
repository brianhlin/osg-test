import os
import pwd
import osgtest.library.core as core
import osgtest.library.osgunittest as osgunittest

class TestGridProxyInit(osgunittest.OSGTestCase):

    def test_01_remove_proxy(self):
        core.skip_ok_unless_installed('voms-clients-cpp')
        # If there is no pre-existing proxy file, the following command will
        # produce error output and have exit status 1; because this is the
        # expected (but not the only valid) case, do not check the output or
        # exit status.  This test exists only to clear out a pre-existing proxy.
        command = ('voms-proxy-destroy', '-debug')
        core.system(command, user=True)

    def test_02_check_usercert_pass(self):
        core.skip_ok_unless_installed('voms-clients-cpp')
        user = pwd.getpwnam(core.options.username)
        userkey = os.path.join(user.pw_dir, '.globus', 'userkey.pem')
        command = ('openssl', 'rsa', '-in', userkey, '-passin', 'pass:', '-text')
        exit_status, _, _ = core.system(command, user=True)
        if exit_status == 0:
            core.system(('voms-proxy-destroy',), user=True)
            self.fail('user cert has no password')

    def test_03_grid_proxy_init(self):
        core.state['proxy.created'] = False
        core.skip_ok_unless_installed('voms-clients-cpp')
        command = ('voms-proxy-init', '-debug')
        password = core.options.password + '\n'
        core.check_system(command, 'Normal voms-proxy-init', user=True, stdin=password)
        core.state['proxy.created'] = True

    def test_04_grid_proxy_info(self):
        core.skip_ok_unless_installed('voms-clients-cpp')
        self.skip_bad_unless(core.state['proxy.created'], 'Proxy creation failed')
        command = ('voms-proxy-info', '-debug')
        core.check_system(command, 'Normal voms-proxy-info', user=True)
