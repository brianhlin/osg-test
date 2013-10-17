import os
import shutil
import unittest

import osgtest.library.core as core
import osgtest.library.files as files
import osgtest.library.service as service
import osgtest.library.osgunittest as osgunittest

class TestStopMySQL(osgunittest.OSGTestCase):

    def test_01_stop_mysqld(self):
        core.skip_ok_unless_installed('mysql-server')
        service.stop('mysqld')

    def test_02_restore_backup(self):
        if not core.options.backupmysql:
            return

        core.skip_ok_unless_installed('mysql-server', 'mysql')

        if core.config['mysql.backup']:
            files.remove(core.config['mysql.datadir'], force=True)
            shutil.move(core.config['mysql.backup'], core.config['mysql.datadir'])
