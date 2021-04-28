
from PySide2.QtCore import QTimer, Qt
from PySide2.QtWidgets import (QAction, QTreeView)
from typing import Callable
class DeveloperMode():
    """
    Modifies components used in main_window to create "Developer Mode"
    """
    def __init__(self):
        self._original_rebuild_action_icon
        self._original_rebuild_function


    def setup_developer_mode(self, rebuild_action: QAction, rebuild_function: Callable, qlibrary_tree_view: QTreeView):
        # add delegate to tree
        # hook up RebuildACtion's trigger to clean all files
        #     source_model.file_dirtied_signal.connect(tree.update)
    # source_model.file_cleaned_signal.connect(tree.update)
        # save action's icone and rebuild function
        # replace rebuild signal/slot connection to  will reimport rebuild function from design
        # dirty file logic stays here
        # hook up tree make QAction Icon red if dirty


    def clean_and_remove_developer_mode:
        # set empty delegate to tree
            #    undo      source_model.file_dirtied_signal.connect(tree.update)
# source_model.file_cleaned_signal.connect(tree.update)
#         self.qlibrary_rebuild_signal.connect(source_model.clean_file)
        # turn off file watcher
        # return original icon to QAction
        # replace rebuild singla/slot with oiriginal rebuild func
        # unhookup tree to file action