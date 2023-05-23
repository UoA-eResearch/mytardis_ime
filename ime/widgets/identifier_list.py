import typing
from typing import List
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget
from ime.models import IIdentifiers
from ime.qt_models import IngestionMetadataModel, PythonListModel
from ime.ui.ui_identifier_list import Ui_IdentifierList
from PyQt5.QtCore import Qt

class IdentifierListModel(PythonListModel):
    object_with_ids: IIdentifiers

    def __init__(self, parent=None):
        super().__init__(parent)
        
    def set_object_with_ids(self, obj: IIdentifiers):
        self.beginResetModel()
        self.object_with_ids = obj
        if obj.identifiers is None:
            obj.identifiers = []
        self.setStringList(obj.identifiers)
        self.endResetModel()

    def setData(self, index: QModelIndex, value: str, role = Qt.ItemDataRole.DisplayRole) -> bool:
        if self.object_with_ids.identifiers is None:
            self.object_with_ids.identifiers = []
        old_id = self.object_with_ids.identifiers[index.row()]
        return self.object_with_ids.update_identifier(old_id, value)

    def removeRows(self, row: int, count: int, parent=...) -> bool:
        if self.object_with_ids.identifiers is None:
            return False
        self.beginRemoveRows(QModelIndex(), row, row+count-1)
        for i in range(0, count):
            # Remove rows from largest index first
            # to avoid being affected by reassigned indices.
            idx = row+count-1-i
            value = self.object_with_ids.identifiers[idx]
            self.object_with_ids.delete_identifier(value)
        self.endRemoveRows()
        return True

class IdentifierList(QWidget):
    def __init__(self, parent: QWidget | None = None,) -> None:
        super().__init__(parent)
        self.ui = Ui_IdentifierList()
        self.ui.setupUi(self)
        self.ui.btnAdd.clicked.connect(self._handle_insert_new)
        self.ui.btnDelete.clicked.connect(self._handle_remove_from_list)
        self._model = IdentifierListModel()
        self.ui.identifierList.setModel(self._model)

    def set_data(self, data: IIdentifiers):
        self.data = data
        if data.identifiers is None:
            data.identifiers = []
        self._model.set_object_with_ids(data)

    def _handle_insert_new(self):
        idx = self._model.rowCount()
        self._model.insertRow(idx)
        model_idx = self._model.index(idx, 0)
        self.ui.identifierList.setCurrentIndex(model_idx)
        self.ui.identifierList.edit(model_idx)

    def _handle_remove_from_list(self):
        idx_list = self.ui.identifierList.selectedIndexes()
        rows_to_remove = [idx.row() for idx in idx_list]
        # Reverse sort the rows to remove, so we're not affected
        # by row index changes.
        rows_to_remove.sort(reverse=True)
        # Check if 
        for row in rows_to_remove:
            self._model.removeRow(row)