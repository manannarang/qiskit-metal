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
"""
File System Model for QLibrary Display
"""

import typing

from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QFileSystemModel, QWidget


class QFileSystemLibraryModel(QFileSystemModel):
    """
    File System Model for displaying QLibrary in MetalGUI
    Has additional FileWatcher added to keep track of edited
    QComponent files and, in developer mode,
    to alert the view/delegate to let the user know these files
    are dirty and refresh the design
    """
    FILENAME = 0  # Column index to display filenames


    def __init__(self, parent: QWidget = None):
        """
        Initializes Model


        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        self.columns = ['QComponents']



    def headerData(self,
                   section: int,
                   orientation: Qt.Orientation,
                   role: int = ...) -> typing.Any:
        """ Set the headers to be displayed.

        Args:
            section (int): Section number
            orientation (Qt orientation): Section orientation
            role (Qt display role): Display role.  Defaults to DisplayRole.

        Returns:
            str: The header data, or None if not found
        """

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.columns):
                    return self.columns[section]

        elif role == Qt.FontRole:
            if section == 0:
                font = QFont()
                font.setBold(True)
                return font

        return super().headerData(section, orientation, role)

