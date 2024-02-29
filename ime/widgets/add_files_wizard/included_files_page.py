import os
from pathlib import Path
import typing
from PySide6 import QtCore

from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PySide6.QtWidgets import QWizardPage
import ime.widgets.add_files_wizard.wizard as afw
from ime.utils import file_size_to_str, st_dev


class IncludedFilesPage(QWizardPage):
    def wizard(self) -> 'afw.AddFilesWizard':
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        """Reimplementation of Qt QWizardPage method for initialising the page.

        Returns:
            None.
        """
        wizard = self.wizard()
        wizard.ui.datafileAddPushButton.clicked.connect(self._handle_add_files_clicked)
        wizard.ui.dirAddPushButton.clicked.connect(self._handle_add_directory_clicked)
        wizard.ui.datafileDeletePushButton.clicked.connect(self._handle_delete_files_clicked)

    def cleanupPage(self) -> None:
        """Reimplementation of Qt QWizardPage method for cleaning up the page.
        Returns:
            None.
        """
        wizard = self.wizard()
        wizard.ui.datafileAddPushButton.clicked.disconnect(self._handle_add_files_clicked)
        wizard.ui.dirAddPushButton.clicked.disconnect(self._handle_add_directory_clicked)
        wizard.ui.datafileDeletePushButton.clicked.disconnect(self._handle_delete_files_clicked)    

    def isComplete(self) -> bool:
        """Reimplementation of Qt QWizardPage method for checking if a
        page is complete. This will only be marked complete when user
        has added files.

        Returns:
            bool: Whether the page is complete.
        """
        # Only allow user to finish when they've chosen some files.
        return self.wizard().ui.datafiletableWidget.rowCount() > 0

    def _handle_add_directory_clicked(self) -> None:
        """Handler for adding a directory of files to the table.

        Returns:
            None
        """
        # Set up a QFileDialog to import a folder.
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        dir = file_dialog.getExistingDirectory()
        if dir == '':
            return
        #options = QFileDialog.Option.DontUseNativeDialog
        #dir_to_add = file_dialog.getExistingDirectory(options=options)
        #if dir_to_add == '':
            # If user didn't choose a folder, exit.
            #return
        filepaths: list[Path] = []
        for root, _, files in os.walk(dir):
        #for root, _, files in os.walk(dir_to_add):
            # Go through all the nested subdirectories. 
            for file in files:
                # Go through file in each nested directory.
                path = Path(os.path.join(root, file))
                # Add the file with a complete path.
                filepaths.append(path)
        # If the user confirms importing all the files, then add
        # files to the table.
        if len(filepaths) < 20:
            # If there are fewer than 20 files in this directory,
            # then add files directly, no need to check.
            self._add_files_to_table(filepaths)
        elif self._display_confirm_import_message(filepaths):
            # If 20 or more, then first check whether the user wants this.
            self._add_files_to_table(filepaths)

    def _handle_delete_files_clicked(self) -> None:
        """Delete files from the table.

        Gets the selected rows from the table, creates a list of QModelIndex objects for those rows.
        Passes each QModelIndex object to removeRow() method to delete that row from the table.

        Returns:
            None.
        """
        index_list = []
        for model_index in self.wizard().ui.datafiletableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.wizard().ui.datafiletableWidget.removeRow(index.row())
        self.completeChanged.emit()

    def _handle_add_files_clicked(self) -> None:
        """Add files to the table.

        Gets the table, calls the open_add_files_dialog() method to open a file dialog and get the list of files to add.
        Passes the table and the list of files to add to the add_file_table_rows() method.

        Returns:
            None.
        """
        files_to_add = self._open_add_files_dialog()
        self._add_files_to_table(files_to_add)

    # Methods related to Add Files and Add Directory below.

    def _open_add_files_dialog(self) -> list[Path]:
        """Open a file dialog and get the list of files to add.

        Creates a file dialog, opens it to allow the user to select files to add.
        Returns the list of QFileInfo objects for the selected files.

        Returns:
            A list of QFileInfo objects for the selected files.
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        filename = file_dialog.getOpenFileNames()
        #options = QFileDialog.Option.DontUseNativeDialog
        #filename = file_dialog.getOpenFileNames(options=options)
        fpath = filename[0]

        new_files = []
        for f in fpath:
            if f == "":
                continue
            path = Path(f)
            if path in new_files:
                continue
            new_files.append(path)
        return new_files

    def _display_confirm_import_message(self, filepaths: list[Path]) -> bool:
        """Displays a confirmation message to check if user wants to proceed with importing
        the files. Returns whether the user has confirmed.

        Args:
            filepaths (list[Path]): The file paths being imported.

        Returns:
            bool: True if the user has confirmed, False if not.
        """
        num_files = len(filepaths)
        confirm_msg = QMessageBox()
        confirm_msg.setWindowTitle("Confirm import folder of files")
        confirm_msg.setText(f"Import {num_files} file{'s' if num_files > 1 else ''}?")
        confirm_msg.setInformativeText("All files in this folder and sub-folders will be imported, with folder structure preserved.")
        confirm_msg.setStandardButtons(typing.cast(QMessageBox.StandardButtons, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel))
        res = confirm_msg.exec()
        return res == QMessageBox.StandardButton.Ok

    def _display_add_files_failed_error(self, correct_drive_path: Path) -> None:
        """Private method that displays an error dialog for failure to import data
        files due to files being stored in a different drive. 

        Args:
            correct_drive_path (Path): The path that files should be located at.
        """
        drive_msg = f"the drive for {correct_drive_path}" 
        drive = correct_drive_path.drive
        if drive != "":
            drive_msg = f"the {drive} drive"
        error_msg = QMessageBox()
        error_msg.setWindowTitle("Can't import data files")
        error_msg.setText("Your data can\'t be imported. Previously imported data "
            f"were stored on {drive_msg}, but the selected data files are "
            "stored in a different drive. All your data needs to be on "
            "the same drive to be found by the ingestion process.")
        error_msg.setInformativeText(f"Please move your data to {drive_msg}, then try again.")
        error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_msg.exec()

    def _validate_files_to_add(self, files_to_add: list[Path]) -> bool:
        """Private method to validate that files are on the same device as workspace.
        If not valid, display an error message and return False.

        Args:
            files_to_add (list[Path]): Files to validate
            workspace_dev_id (int): Workspace's device ID

        Returns:
            bool: Whether these files are valid to add
        """
        # Figure out the workspace path. 
        # If there isn't any yet, we use the first file 
        # from the currently selected list. 
        first_file_path = files_to_add[0].parent
        workspace_path = self._workspace_path() or first_file_path
        workspace_device_id = st_dev(workspace_path)
        for file in files_to_add:
            # Go through each file to check whether they are stored
            # on the same drive.
            file_dev = st_dev(file)
            if file_dev != workspace_device_id:
                self._display_add_files_failed_error(workspace_path)
                return False
        return True

    def _workspace_path(self) -> typing.Optional[Path]:
        """Private method for getting the workspace path. If the ingestion
        file is already saved, then take the path of the ingestion file as
        the path. If not, then take a previously added file's path. Return
        None if that doesn't exist.

        Returns:
            typing.Optional[Path]: The workspace path, or None if there isn't one
            yet.
        """
        table = self.wizard().ui.datafiletableWidget
        # Check all datafiles are from same drive.
        data = self.wizard().metadataModel.metadata
        data_path = data.data_path
        if data_path is not None:
            # If there is an workspace path...
            return data_path
        else:
            # If we are adding to a blank file...
            if table.rowCount() > 0:
                # If there are already other files the user has
                # imported in this dialog, we use the first file's
                # drive.
                data_path = Path(table.item(0,2).text()).parent
                return data_path
        
    def _add_files_to_table(self, files_to_add: list[Path]) -> None:
        """Private method to add files to the included files table.

        Args:
            files_to_add (list[Path]): The files to add, as Paths.
        """
        if len(files_to_add) == 0:
            # If there are no files to add, then do not add.
            return
        if not self._validate_files_to_add(files_to_add):
            # If the files aren't valid, then do not add.
            return
        self._add_file_table_rows(files_to_add)
        self.completeChanged.emit()

    def _add_file_table_rows(self, files_to_add: list[Path]) -> None:
        """Add rows to the table.

        Gets the table and the list of files to add.
        Iterates over the list of files to add and creates a row in the table for each file.
        Sets the filename, size, and file path as items in the row.

        Args:
            files_to_add: A list of QFileInfo objects to create rows for.

        Returns:
            None.
        """
        table = self.wizard().ui.datafiletableWidget
        # Need to start inserting rows after existing rows.
        initial_row_count = table.rowCount()
        # Grow the table to fit new rows.
        table.setRowCount(initial_row_count + len(files_to_add))
        new_row_index = 0
        for file in files_to_add:
            # Create corresponding cells for file and insert them into table.
            name_cell = QTableWidgetItem(file.name)
            size = file.stat().st_size
            size_str = file_size_to_str(size)
            #md5sum = self._calculate_md5(file)
            size_cell = QTableWidgetItem(size_str)
            # Store actual size value in cell. 
            size_cell.setData(QtCore.Qt.ItemDataRole.UserRole, size)
            fpath_cell = QTableWidgetItem(str(file))
            # Insert cells into the table.
            row_index = initial_row_count + new_row_index
            table.setItem(row_index, 0, name_cell)
            table.setItem(row_index, 1, size_cell)
            table.setItem(row_index, 2, fpath_cell)
            # Increment for the next row
            new_row_index += 1
