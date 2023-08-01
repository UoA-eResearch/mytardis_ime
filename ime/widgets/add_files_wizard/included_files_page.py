
import os
from pathlib import Path
import typing
from PyQt5 import QtCore

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QWizardPage
import ime.widgets.add_files_wizard.wizard as afw
from ime.utils import file_size_to_str, st_dev


class IncludedFilesPage(QWizardPage):
    def wizard(self) -> 'afw.AddFilesWizard':
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        wizard = self.wizard()
        wizard.ui.datafileAddPushButton.clicked.connect(self.addFiles_handler)
        wizard.ui.dirAddPushButton.clicked.connect(self.addDir_handler)
        wizard.ui.datafileDeletePushButton.clicked.connect(self.deleteFiles_handler)

    def cleanupPage(self) -> None:
        wizard = self.wizard()
        wizard.ui.datafileAddPushButton.clicked.disconnect(self.addFiles_handler)
        wizard.ui.dirAddPushButton.clicked.disconnect(self.addDir_handler)
        wizard.ui.datafileDeletePushButton.clicked.disconnect(self.deleteFiles_handler)

    def add_file_table_rows(self, table: QTableWidget,files_to_add: list[Path]) -> None:
        """Add rows to the table.

        Gets the table and the list of files to add.
        Iterates over the list of files to add and creates a row in the table for each file.
        Sets the filename, size, and file path as items in the row.

        Args:
            table: A QTableWidget object to add rows to.
            files_to_add: A list of QFileInfo objects to create rows for.

        Returns:
            None.
        """
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

    def addDir_handler(self) -> None:
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
            # If user didn't choose a folder, exit.
            return
        filepaths: list[Path] = []
        for root, _, files in os.walk(dir):
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
            self.add_files_to_table(filepaths)
        elif self._display_confirm_import_message(filepaths):
            # If 20 or more, then first check whether the user wants this.
            self.add_files_to_table(filepaths)

    def open_add_files_dialog(self) -> list[Path]:
        """Open a file dialog and get the list of files to add.

        Creates a file dialog, opens it to allow the user to select files to add.
        Returns the list of QFileInfo objects for the selected files.

        Returns:
            A list of QFileInfo objects for the selected files.
        """
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        filename = file_dialog.getOpenFileNames()  
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

    def addFiles_handler(self) -> None:
        """Add files to the table.

        Gets the table, calls the open_add_files_dialog() method to open a file dialog and get the list of files to add.
        Passes the table and the list of files to add to the add_file_table_rows() method.

        Returns:
            None.
        """
        files_to_add = self.open_add_files_dialog()
        self.add_files_to_table(files_to_add)

    def display_add_files_failed_error(self, correct_drive_path: Path):
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
        
    def add_files_to_table(self, files_to_add: list[Path]) -> None:
        table = self.wizard().ui.datafiletableWidget
        if len(files_to_add) == 0:
            return
        # Check all datafiles are from same drive.
        data_path = self.wizard().metadataModel.metadata.data_path
        if data_path is not None:
            # If there is an effective path, use that to determine
            # the drive the data should be stored on.
            data_dev = st_dev(data_path)
        else:
            # If we are adding to a blank file...
            if table.rowCount() > 0:
                # If there are already other files the user has
                # imported in this dialog, we use the first file's
                # drive.
                data_path = Path(table.item(0,2).text()).parent
                data_dev = st_dev(data_path)
            else:
                # If there aren't any files already imported,
                # we use the first file from the currently selected
                # list. 
                data_path = files_to_add[0].parent
                data_dev = st_dev(data_path)
        for file in files_to_add:
            # Go through each file to check whether they are stored
            # on the same drive.
            file_dev = st_dev(file)
            if file_dev != data_dev:
                self.display_add_files_failed_error(data_path)
                return
        self.add_file_table_rows(table,files_to_add)


    def deleteFiles_handler(self):
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
