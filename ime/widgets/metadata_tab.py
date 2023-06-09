from typing import List
from PyQt5.QtCore import QItemSelection, QLine, QSignalBlocker, pyqtSlot

from ime.bindable import IBindableInput
from ime.ui.ui_metadata_tab import Ui_MetadataTab
from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem, QWidget, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
from ime.models import IMetadata
import logging

from ime.utils import setup_header_layout

class MetadataTab(QWidget, IBindableInput):
    """A tab widget for displaying and editing metadata information for an object."""
    metadata_object: IMetadata
    ui: Ui_MetadataTab

    def __init__(self, parent=None):
        """Initializes the metadata tab with the given parent widget."""
        super(QWidget, self).__init__(parent)
        self.ui = Ui_MetadataTab()
        self.ui.setupUi(self)
        self.ui.metadata_table.cellChanged.connect(self._handle_cell_changed)
        self.ui.schemaLineEdit.textChanged.connect(self.handle_schema_changed)
        self.ui.metadata_table.selectionModel().selectionChanged.connect(self.handle_selection_changed)
        self.ui.add_row_btn.clicked.connect(self._handle_add_row_click)
        self.ui.remove_rows_btn.clicked.connect(self.handle_remove_rows_click)
        self.ui.notes_textedit.textChanged.connect(self.handleNotes_changed)
        setup_header_layout(self.ui.metadata_table.horizontalHeader())

    def handle_schema_changed(self, schema: str):
        """Handles the schema text box changing."""
        self.metadata_object.object_schema = self.ui.schemaLineEdit.text()

    def handleNotes_changed(self):
        self.metadata_object.metadata['Notes'] = self.ui.notes_textedit.toPlainText()

    def add_insert_metadata_row(self):
        """Adds an empty row to the metadata table."""
        table = self.ui.metadata_table
        # key_item, val_item = self.get_metadata_row("", "")
        key_item = QTableWidgetItem("")
        val_item = QTableWidgetItem("")
        row_idx = table.rowCount()
        table.setRowCount(row_idx + 1)
        table.setItem(row_idx, 0, key_item)
        table.setItem(row_idx, 1, val_item)
    
    def get_metadata_row(self, key: str, val: str):
        """Returns a key-value metadata row as QTableWidgetItem objects.

        Args:
            key (str): The key for the metadata field.
            val (str): The value for the metadata field.

        Returns:
            tuple(QTableWidgetItem, QTableWidgetItem): The key and value QTableWidgetItem objects.
        """
        # key_edit = QLineEdit()
        # key_edit.setText(key)
        # key_edit.setPlaceholderText("Name for the field, e.g. Batch number")
        key_item = QTableWidgetItem(key)
        # Use the UserRole to store another copy of the key,
        # so when user has edited the item we can find the
        # associated value.
        key_item.setData(Qt.ItemDataRole.UserRole, key)
        # key_item.setFlags(Qt.ItemFlag.ItemIsSelectable)
        # val_edit = QLineEdit()
        # val_edit.setText(val)
        # val_edit.setPlaceholderText("Value for the field, e.g. 400")
        val_item = QTableWidgetItem(val)
        return key_item, val_item

    def handle_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        """Enables the "Remove Rows" button if rows are selected in the metadata table.

        Args:
            selected (QItemSelection): The selected item(s).
            deselected (QItemSelection): The deselected item(s).
        """
        table = self.ui.metadata_table
        selected_rows = table.selectionModel().selectedRows()
        if (len(selected_rows) == 1 and 
            selected_rows[0].row() == table.rowCount() - 1):
            # If only the empty row is selected, do not enable.
            self.ui.remove_rows_btn.setEnabled(False)
            return
        self.ui.remove_rows_btn.setEnabled(len(selected_rows) > 0)

    def _handle_cell_changed(self, row: int, col: int):
        """Private method that handles the change event for a cell in the metadata table.

        Args:
            row (int): The row index of the changed cell.
            col (int): The column index of the changed cell.
        """
        table = self.ui.metadata_table
        metadata = self.metadata_object.metadata
        cell = table.item(row, col)
        cell_val = cell.text()
        if col == 0:
            if row != table.rowCount() - 1:
                old_name = cell.data(Qt.ItemDataRole.UserRole)
                if cell_val in metadata:
                    # If the user has duplicated a name,
                    # do not modify underlying data and
                    # undo the change.
                    with QSignalBlocker(table):
                        cell.setText(old_name)
                        return
                metadata_value = self.metadata_object.metadata[old_name]
                del self.metadata_object.metadata[old_name]
                self.metadata_object.metadata[cell_val] = metadata_value
                with QSignalBlocker(table):
                    cell.setData(Qt.ItemDataRole.UserRole, cell_val)
            else:
                # This is a new metadata key being inserted!
                if cell_val in metadata:
                    # If the key already exists, undo the editing.
                    with QSignalBlocker(table):
                        cell.setText('')
                    return
                with QSignalBlocker(table):
                    # Add a new row to the bottom.
                    # Use a signal blocker to prevent a signal being sent
                    # causing recursion
                    metadata[cell_val] = ''
                    self.add_insert_metadata_row()
                    cell.setData(Qt.ItemDataRole.UserRole, cell_val)
        else:
            # The user has edited a metadata value
            # TODO Empty key fields should be checked and enforced!
            # TODO Enforce unique keys.
            key = table.item(row, 0).text()
            if key == "":
                return
            self.metadata_object.metadata[key] = cell_val

    def _handle_add_row_click(self) -> None:
        """Private method for handling when the Add button is
        clicked. Focuses the editing on the new edit row.
        """
        table = self.ui.metadata_table
        edit_row_name_cell = table.model().index(table.rowCount() - 1, 0)
        self.ui.metadata_table.edit(edit_row_name_cell)

    def handle_remove_rows_click(self):
        """Handles the click event for the Remove Rows button."""
        table = self.ui.metadata_table
        items = table.selectedItems()
        # Extract the rows that need to be deleted.
        rows = set([item.row() for item in items])
        for row in rows:
            if row == table.rowCount() - 1:
                # Skip deleting the empty row.
                continue
            key = table.item(row, 0).text()
            self.metadata_object.metadata.pop(key)
            table.removeRow(row)

    def update_metadata_object(self, metadata_obj: IMetadata):
        """Updates the object this tab is modifying.

        Args:
            metadata_obj (IMetadata): The metadata object to update the tab with.
        """
        # Block table change signals while object is being updated.
        with QSignalBlocker(self.ui.metadata_table):
            table = self.ui.metadata_table
            # First, clear all existing rows (if any) that's already
            # in the tab.
            table.clearContents()
            table.setRowCount(0)
            # Then, populate table with new items 
            metadata = metadata_obj.metadata                
            num_new = len(metadata)
            if "Notes" in metadata:
                # Remove a line if there are Notes.
                num_new = num_new - 1
            table.setRowCount(num_new)
            row_idx = 0
            for key,val in metadata.items():
                if key == "Notes":
                    # Skip the notes field. Display it in the separate notes
                    # section instead
                    continue
                key_item, val_item = self.get_metadata_row(key, str(val))
                table.setItem(row_idx, 0, key_item)
                table.setItem(row_idx, 1, val_item)
                row_idx += 1
            self.add_insert_metadata_row()
            self.metadata_object = metadata_obj
        # Update schema
        object_schema_value = metadata_obj.object_schema
        self.ui.schemaLineEdit.setText(str(object_schema_value))
        # Update notes section
        if 'Notes' in metadata_obj.metadata:
            notes = metadata_obj.metadata['Notes']
        else:
            notes = ""
        with QSignalBlocker(self.ui.notes_textedit):
            self.ui.notes_textedit.setText(notes)