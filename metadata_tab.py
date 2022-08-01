from typing import List
from PyQt5.QtCore import QLine
from ui.MetadataTab import Ui_MetadataTab
from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem, QUndoStack, QWidget, QLineEdit
from PyQt5.QtCore import pyqtSignal
from models import IMetadata
import logging

# class MetadataRow():
#     def __init__(self, key: str, val: str):
#         self.keywidget = QLineEdit()
#         self.valwidget = QLineEdit()
#         self.rowwidget = QHBoxLayout()
#         self.keywidget.setText(str(key))
#         self.valwidget.setText(str(val))
#         self.rowwidget.addChildWidget(self.keywidget)
#         self.rowwidget.addChildWidget(self.valwidget)

#     def render(self, parent: QWidget):
#         parent.
#         self.rowwidget.setParent(parent)

class MetadataTab(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.ui = Ui_MetadataTab()
        self.ui.setupUi(self)

    def add_insert_metadata_row(self):
        table = self.ui.metadata_table
        key_item, val_item = self.get_metadata_row("", "")
        row_idx = table.rowCount()
        table.setRowCount(row_idx + 1)
        table.setItem(row_idx, 0, key_item)
        table.setItem(row_idx, 1, val_item)
    
    def get_metadata_row(self, key: str, val: str):
            # key_edit = QLineEdit()
            # key_edit.setText(key)
            # key_edit.setPlaceholderText("Name for the field, e.g. Batch number")
            key_item = QTableWidgetItem(key)
            # val_edit = QLineEdit()
            # val_edit.setText(val)
            # val_edit.setPlaceholderText("Value for the field, e.g. 400")
            val_item = QTableWidgetItem(val)
            return key_item, val_item


    def update_object(self, metadata_obj: IMetadata):
        """Updates the object this tab is modifying."""
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
