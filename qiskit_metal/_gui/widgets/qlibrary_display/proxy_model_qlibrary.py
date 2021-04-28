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
Proxy Model to clean display of QComponents in Library tab
"""

import typing

from PySide2.QtCore import QModelIndex, QSortFilterProxyModel, Qt, QSize
from PySide2.QtWidgets import QWidget


class LibraryFileProxyModel(QSortFilterProxyModel):
    """
    Proxy Model to clean up display for QFileSystemLibraryModel
    """

    def __init__(self, parent: QWidget = None):
        """Proxy Model for cleaning up QFileSystemLibraryModel for displaying GUI's QLibrary
        Args:
            parent: Parent widget
        """

        super().__init__(parent)

        # finds all files that
        # (Aren't hidden (begin w/ .), don't begin with __init__, don't begin with _template, etc. AND end in .py)  OR (don't begin with __pycache__ and don't have a '.' in the name   # pylint: disable=line-too-long
        # (QComponent files) OR (Directories)
        self.accepted_files__regex = r"(^((?!\.))(?!__init__)(?!_template)(?!__pycache__).*\.py)|(?!__pycache__)(?!base)(^([^.]+)$)"  # pylint: disable=line-too-long
        self.setFilterRegExp(self.accepted_files__regex)

    def filterAcceptsColumn(self, source_column:int, source_parent:QModelIndex) -> bool: #pylint: disable=unused-argument
        """
        Filters out unwanted file information in display
        Args:
            source_column: Display column in question
        Returns:
            bool: Whether to display column


        """
        # Won't show Size, Kind, Date Modified, etc. for QFileSystemModel
        if source_column > self.sourceModel().FILENAME:
            return False

        return True
