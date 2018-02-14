import osgtest.library.core as core
import osgtest.library.osgunittest as osgunittest

class TestGridProxyDestroy(osgunittest.OSGTestCase):

    def test_01_check_proxy(self):
        core.skip_ok_unless_installed('voms-clients-cpp')
        self.skip_ok_unless(core.state['proxy.created'], 'missing proxy')
        command = ('voms-proxy-destroy', '-debug')
        core.check_system(command, 'Run voms-proxy-destroy', user=True)
