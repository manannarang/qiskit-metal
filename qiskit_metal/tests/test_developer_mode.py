# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable-msg=unnecessary-pass
# pylint: disable-msg=protected-access
# pylint: disable-msg=pointless-statement
# pylint: disable-msg=too-many-public-methods
# pylint: disable-msg=broad-except
# pylint: disable-msg=invalid-name
# pylint: disable-msg=import-error
"""Qiskit Metal unit tests analyses functionality."""

from PySide2 import QtTest
from PySide2.QtCore import QObject
import unittest
import os , shutil
from qiskit_metal._gui.widgets.developer_mode.qlibrary_file_watcher_holder import QLibraryFileWatcherHolder
from qiskit_metal.tests.test_data import test_dir
from qiskit_metal import designs, MetalGUI




class TestQt(QObject):



class TestDevModeQLibraryFileWatcher(unittest.TestCase):
    """Unit test class."""

    @classmethod
    def initTestCase(cls) -> None:
        cls.design = designs.DesignPlanar()
        cls.gui = MetalGUI(cls.design)
        print(test_dir.__file__)
        init_test_dir_abs_path = os.path.abspath(test_dir.__file__)
        test_dir_abs_path = init_test_dir_abs_path.split('__init__.py')[0]
        cls.TEST_DIR_ROOT = test_dir_abs_path
        cls.TEST_DIR_FOLDERNAME = test_dir.__name__


    def init(self):
        """Setup unit test."""
        self.pre_existing_files = ['TaylorSwift', "ZTao", "SonTung"]
        for pfile in self.pre_existing_files:
            if not os.path.isfile(os.path.join(self.TEST_DIR_ROOT, pfile)):
                with open(os.path.join(self.TEST_DIR_ROOT, pfile), 'w') as new_f:
                    new_f.write("test")

        self.fw_holder = QLibraryFileWatcherHolder(self.TEST_DIR_ROOT)
        # getting absolute path of QLibrary folder

    # def tearDown(self):
    #     """Tie any loose ends."""
    #     self.clean_test_directory()

    def cleanup(self):
        for filename in os.listdir(self.TEST_DIR_ROOT):
            file_path = os.path.join(self.TEST_DIR_ROOT, filename)
            if '__init__.py' not in file_path:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

    def add_new_file(self, filename):
        with open(os.path.join(self.TEST_DIR_ROOT, filename), 'w') as f:
            f.write("""I don't wanna let your drama
            Come and bring me down""")

    def remove_file(self, filename):
        os.remove(os.path.join(self.TEST_DIR_ROOT, filename))

    def test_add_new_file_to_dir(self):
        new_file = "MaybeAtTheEndOfTheWeekend?"
        self.add_new_file(new_file)
        assert new_file in self.fw_holder.dirtied_files
        assert new_file in self.fw_holder.file_system_watcher.files()


    def test_remove_existing_file(self):
        rmed_file = self.pre_existing_files[0]
        self.remove_file(rmed_file)
        assert rmed_file in self.fw_holder.dirtied_files
        assert rmed_file not in self.fw_holder.file_system_watcher.files()

    def test_edit_prexisting_file(self):
        edit_file = self.pre_existing_files[0]
        with open(os.path.join(self.TEST_DIR_ROOT, edit_file), 'w') as f:
            f.write("Cozy Coffee Shop Jazz")

        print(self.fw_holder.file_system_watcher.files())
        print(self.pre_existing_files[0])
        print(self.fw_holder.dirtied_files)

        assert edit_file in self.fw_holder.dirtied_files
        assert edit_file in self.fw_holder.file_system_watcher.files()

    def test_check_clean_all_files(self):
        self.fw_holder.clean_all_files()
        assert len(self.fw_holder.dirtied_files) == 0


if __name__ == '__main__':
    unittest.main(verbosity=2)
    print("I don't wanna let your drama bring me down. Maybe at the end of the weekend? ;) ")
