import os
import osgtest.library.core as core
import osgtest.library.files as files
import unittest

class TestStopPBS(unittest.TestCase):

    required_rpms = ['torque-mom',
                     'torque-server',
                     'torque-scheduler']

    def test_01_stop_mom(self):
        if core.missing_rpm(*self.required_rpms):
            return
        if core.state['torque.pbs-mom-running'] == False:
            core.skip('did not start pbs mom server')
            return

        command = ('service', 'pbs_mom', 'stop')
        stdout, _, fail = core.check_system(command, 'Stop pbs mom')
        self.assert_(stdout.find('error') == -1, fail)
        self.assert_(not os.path.exists(core.config['torque.mom-lockfile']),
                     'PBS mom run lock file still present')

        core.state['torque.pbs-mom-running'] = False

    def test_02_stop_server(self):
        if core.missing_rpm(*self.required_rpms):
            return
        if core.state['torque.pbs-server-running'] == False:
            core.skip('did not start pbs server')
            return

        command = ('service', 'pbs_server', 'stop')
        stdout, _, fail = core.check_system(command, 'Stop pbs server')
        self.assert_(stdout.find('error') == -1, fail)
        self.assert_(not os.path.exists(core.config['torque.pbs-lockfile']),
                     'PBS server run lock file still present')

        core.state['torque.pbs-server-running'] = False

    def test_03_stop_scheduler(self):
        if core.missing_rpm(*self.required_rpms):
            return
        if core.state['torque.pbs-sched-running'] == False:
            core.skip('did not start pbs scheduler')
            return

        command = ('service', 'pbs_sched', 'stop')
        stdout, _, fail = core.check_system(command, 'Stop pbs scheduler')
        self.assert_(stdout.find('error') == -1, fail)
        self.assert_(not os.path.exists(core.config['torque.sched-lockfile']),
                     'PBS server run lock file still present')

        files.restore('/var/torque/server_priv/nodes', 'pbs')
        core.state['torque.pbs-sched-running'] = False
