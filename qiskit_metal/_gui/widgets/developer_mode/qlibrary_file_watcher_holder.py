import os

from PySide2.QtCore import QFileSystemWatcher, Signal
from PySide2.QtWidgets import QWidget


class QLibraryFileWatcher(QFileSystemWatcher):

    file_dirtied_signal = Signal()
    file_cleaned_signal = Signal()

    def __init__(self, qlibrary_path: str, parent: QWidget = None):
        """
        Initializes Model

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.dirtied_files = dict()
        self.ignored_substrings = {'.cpython', '__pycache__', '__init__'}
        self.qlibrary_path = qlibrary_path
        self.hasanythingeverbeendirty = False
        self._set_root_path(self.qlibrary_path)



    def _set_root_path(self, path: str):
        """
        Sets FileWatcher on root path
        Args:
            path: Root path

        """
        for root, _, files in os.walk(path):
            # do NOT use directory changed -- fails for some reason
            for name in files:
                if self.is_trackable_file(name):
                    self.addPath(os.path.join(root, name))

        print(
            f"Successfully connected: {self.fileChanged.connect(self.set_file_dirty)}"
        )
        print(
            f"Successfully connected: {self.directoryChanged.connect(self.set_file_dirty)}"
        )


        with open(
                os.path.join(self.qlibrary_path,
                             "The 1975"), 'w') as f:
            f.write("rip")
            f.flush()
            os.fsync(f.fileno())
        import time
        time.sleep(2)
        print(f"creatied: {self.hasanythingeverbeendirty}")


    def set_file_dirty(self, filepath: str):
        self.hasanythingeverbeendirty = True
        """
        Dirties file and re-adds edited file to the FileWatcher
        Emits file_dirtied_signal
        Args:
            filepath: Dirty file

        """
        print("dirtying")
        if filepath not in self.files():
            if os.path.exists(filepath):
                self.addPath(filepath)
        filename = self.filepath_to_filename(filepath)
        if not self.is_trackable_file(filename):
            return

        sep = os.sep if os.sep in filepath else '/'
        for file in filepath.split(sep):

            if file in self.dirtied_files:
                self.dirtied_files[file].add(filename)
            else:
                self.dirtied_files[file] = {filename}

        # overwrite filename entry from above
        self.dirtied_files[filename] = {filepath}

        self.file_dirtied_signal.emit()

    def is_file_dirty(self, filepath: str) -> bool:
        """
        Checks whether file is dirty
        Args:
            filepath: File in question

        Returns: Whether file is dirty

        """
        filename = self.filepath_to_filename(filepath)
        return filename in self.dirtied_files

    def filepath_to_filename(self, filepath: str) -> str:  # pylint: disable=R0201, no-self-use
        """
        Gets just the filename from the full filepath
        Args:
            filepath: Full file path

        Returns: Filename

        """

        # split on os.sep and / because PySide appears to sometimes use / on
        # certain Windows
        filename = filepath.split(os.sep)[-1].split('/')[-1]
        if '.py' in filename:
            return filename[:-len('.py')]
        return filename

    def clean_file(self, filepath: str):
        """
        Remove file from the _dirtied_files dictionary
        and remove any parent files who are only dirty due to
        this file. Emits file_cleaned_signal.
        Args:
            filepath: Clean file path

        """
        filename = self.filepath_to_filename(filepath)
        self.dirtied_files.pop(filename, f"failed to pop {filepath}")

        sep = os.sep if os.sep in filepath else '/'
        for file in filepath.split(sep):
            if file in self.dirtied_files:
                # if file was in dirtied files only because it is a parent dir
                # of filename, remove
                self.dirtied_files[file].discard(filename)

                if len(self.dirtied_files[file]) < 1:
                    self.dirtied_files.pop(file)
        self.file_cleaned_signal.emit()

    def clean_all_files(self):
        self.dirtied_files = {}

    def is_trackable_file(self, file: str):
        """
        Whether it's a file the FileWatcher should track
        Args:
            file: Filename

        Returns: Whether file is one the FileWatcher should track

        """
        for sub in self.ignored_substrings:
            if sub in file:
                return False
        return True
