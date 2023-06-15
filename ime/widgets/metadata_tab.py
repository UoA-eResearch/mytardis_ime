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

    def __init__(self, parent=None) -> None:
        """Initializes the metadata tab with the given parent widget."""
        super(QWidget, self).__init__(parent)
        self.ui = Ui_MetadataTab()
        self.ui.setupUi(self)
        self.ui.metadata_table.cellChanged.connect(self.handle_cell_changed)
        self.ui.schemaLineEdit.textChanged.connect(self.handle_schema_changed)
        self.ui.metadata_table.selectionModel().selectionChanged.connect(self.handle_selection_changed)
        self.ui.remove_rows_btn.clicked.connect(self.handle_remove_rows_click)
        setup_header_layout(self.ui.metadata_table.horizontalHeader())

    def handle_schema_changed(self, schema: str) -> None:
        """Handles the schema text box changing."""
        self.metadata_object.object_schema = self.ui.schemaLineEdit.text()

    def add_insert_metadata_row(self) -> None:
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
        key_item.setFlags(Qt.ItemFlag.ItemIsSelectable)
        # val_edit = QLineEdit()
        # val_edit.setText(val)
        # val_edit.setPlaceholderText("Value for the field, e.g. 400")
        val_item = QTableWidgetItem(val)
        return key_item, val_item

    def handle_selection_changed(self, selected: QItemSelection, deselected: QItemSelection) -> None:
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

    def handle_cell_changed(self, row: int, col: int) -> None:
        """Handles the change event for a cell in the metadata table.

        Args:
            row (int): The row index of the changed cell.
            col (int): The column index of the changed cell.
        """
        table = self.ui.metadata_table
        cell = table.item(row, col)
        cell_val = cell.text()
        if col == 0:
            # This is a new metadata key being inserted!
            # Disable editing of key name
            with QSignalBlocker(self.ui.metadata_table):
                cell.setFlags(Qt.ItemFlag.ItemIsSelectable)
                # Add a new row to the bottom.
                # Use a signal blocker to prevent a signal being sent
                # causing recursion
                self.add_insert_metadata_row()
        else:
            # The user has edited a metadata value
            # TODO Empty key fields should be checked and enforced!
            # TODO Enforce unique keys.
            key = table.item(row, 0).text()
            if key == "":
                return
            self.metadata_object.metadata[key] = cell_val

    def handle_remove_rows_click(self) -> None:
        """Handles the click event for the Remove Rows button."""
        table = self.ui.metadata_table
        items = table.selectedItems()
        for item in items:
            row = item.row()
            if row == table.rowCount() - 1:
                # Skip deleting the empty row.
                continue
            key = table.item(row, 0).text()
            self.metadata_object.metadata.pop(key)
            table.removeRow(row)

    def update_metadata_object(self, metadata_obj: IMetadata) -> None:
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
            table.setRowCount(num_new)
            row_idx = 0
            for key,val in metadata.items():
                key_item, val_item = self.get_metadata_row(key, str(val))
                table.setItem(row_idx, 0, key_item)
                table.setItem(row_idx, 1, val_item)
                row_idx += 1
            self.add_insert_metadata_row()
            self.metadata_object = metadata_obj
        # Update schema
        object_schema_value = metadata_obj.object_schema
        self.ui.schemaLineEdit.setText(str(object_schema_value))
