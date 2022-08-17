from typing import List
from PyQt5.QtCore import QItemSelection, QLine, QSignalBlocker, pyqtSlot

from ime.bindable import IBindableInput
from .ui_metadata_tab import Ui_MetadataTab
from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem, QUndoStack, QWidget, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
from ime.models import IMetadata
import logging

class MetadataTab(QWidget, IBindableInput):
    metadata_object: IMetadata
    ui: Ui_MetadataTab

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.ui = Ui_MetadataTab()
        self.ui.setupUi(self)
        self.ui.metadata_table.cellChanged.connect(self.handle_cell_changed)
        self.ui.metadata_table.selectionModel().selectionChanged.connect(self.handle_selection_changed)
        self.ui.remove_rows_btn.clicked.connect(self.handle_remove_rows_click)

    def add_insert_metadata_row(self):
        table = self.ui.metadata_table
        # key_item, val_item = self.get_metadata_row("", "")
        key_item = QTableWidgetItem("")
        val_item = QTableWidgetItem("")
        row_idx = table.rowCount()
        table.setRowCount(row_idx + 1)
        table.setItem(row_idx, 0, key_item)
        table.setItem(row_idx, 1, val_item)
    
    def get_metadata_row(self, key: str, val: str):
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

    def handle_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        selected_rows = self.ui.metadata_table.selectionModel().selectedRows()
        self.ui.remove_rows_btn.setEnabled(len(selected_rows) > 0)

    def handle_cell_changed(self, row: int, col: int):
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

    def handle_remove_rows_click(self):
        table = self.ui.metadata_table
        items = table.selectedItems()
        for item in items:
            row = item.row()
            key = table.item(row, 0).text()
            self.metadata_object.metadata.pop(key)
            table.removeRow(row)

    def update_metadata_object(self, metadata_obj: IMetadata):
        """Updates the object this tab is modifying."""
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

