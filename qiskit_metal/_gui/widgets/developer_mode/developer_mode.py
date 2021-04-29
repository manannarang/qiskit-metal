
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
        pass
        # add delegate to tree
        # hook up RebuildACtion's trigger to clean all files
        #     source_model.file_dirtied_signal.connect(tree.update)
    # source_model.file_cleaned_signal.connect(tree.update)
        # save action's icone and rebuild function
        # replace rebuild signal/slot connection to  will reimport rebuild function from design
        # dirty file logic stays here
        # hook up tree make QAction Icon red if dirty


    def clean_and_remove_developer_mode(self):
        pass
        # set empty delegate to tree
            #    undo      source_model.file_dirtied_signal.connect(tree.update)
# source_model.file_cleaned_signal.connect(tree.update)
#         self.qlibrary_rebuild_signal.connect(source_model.clean_file)
        # turn off file watcher
        # return original icon to QAction
        # replace rebuild singla/slot with oiriginal rebuild func
        # unhookup tree to file action


    def _refresh_component_build(self, qis_abs_path):
        """Reresh build for a component along a given path.

        Args:
            qis_abs_path (str): Absolute component path.
        """
        self.design.reload_and_rebuild_components(qis_abs_path)
        # Table models
        self.ui.tableComponents.model().refresh()

        # Redraw plots
        self.refresh_plot()
        self.autoscale()



    def refresh_everything(self):
        """Refresh everything."""

        df = self.ui.dockLibrary.library_model.dirtied_files
        values = {list(df[k])[0] for k in df.keys()}

        for file in values:  # dirtied_files size changes during clean_file
            if '.py' in file:
                file = file[file.index('qiskit_metal'):]
                self.design.reload_and_rebuild_components(file)
                self.ui.dockLibrary.library_model.clean_file(file)
        self.refresh()
        self.autoscale()