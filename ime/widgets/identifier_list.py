from PyQt5.QtCore import QItemSelection, QModelIndex
from PyQt5.QtWidgets import QWidget
from PyQt5.sip import delete
from ime.models import IIdentifiers
from ime.qt_models import PythonListModel
from ime.ui.ui_identifier_list import Ui_IdentifierList
from PyQt5.QtCore import Qt

class IdentifierListModel(PythonListModel):
    object_with_ids: IIdentifiers

    def __init__(self, parent=None):
        super().__init__(parent)
        
    def set_object_with_ids(self, obj: IIdentifiers):
        """Set the backing model this list is used for.

        Args:
            obj (IIdentifiers): The Identifiers list object to use.
        """
        self.beginResetModel()
        self.object_with_ids = obj
        if obj.identifiers is None:
            obj.identifiers = []
        self.setStringList(obj.identifiers)
        self.endResetModel()

    def setData(self, index: QModelIndex, value: str, role = Qt.ItemDataRole.DisplayRole) -> bool:
        """Override method for setData in the Qt Model. This is the function
        for updating an identifier.

        Args:
            index (QModelIndex): The index for the cell currently being edited.
            value (str): The new identifier value.
            role (ItemDataRole, optional): The Qt item data role for the data being edited. Defaults to Qt.ItemDataRole.DisplayRole.

        Returns:
            bool: Whether it was successful.
        """
        if self.object_with_ids.identifiers is None:
            self.object_with_ids.identifiers = []
        old_id = self.object_with_ids.identifiers[index.row()]
        return self.object_with_ids.update(old_id, value)

    def removeRows(self, row: int, count: int, parent=...) -> bool:
        if self.object_with_ids.identifiers is None:
            return False
        self.beginRemoveRows(QModelIndex(), row, row+count-1)
        for i in range(0, count):
            # Remove rows from largest index first
            # to avoid being affected by reassigned indices.
            idx = row+count-1-i
            value = self.object_with_ids.identifiers[idx]
            self.object_with_ids.delete(value)
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
        self.ui.btnDelete.setDisabled(True)
        self.ui.identifierList.selectionModel().selectionChanged.connect(self._handle_select_change)

    def set_data(self, data: IIdentifiers):
        """Sets the identifiers to display by the widget.

        Args:
            data (IIdentifiers): The identifiers to display.
        """
        self.data = data
        if data.identifiers is None:
            data.identifiers = []
        self._model.set_object_with_ids(data)

    def _handle_insert_new(self):
        """Private method for handling Add button clicked.
        """
        idx = self._model.rowCount()
        self._model.insertRow(idx)
        model_idx = self._model.index(idx, 0)
        self.ui.identifierList.setCurrentIndex(model_idx)
        self.ui.identifierList.edit(model_idx)

    def _handle_remove_from_list(self):
        """Private method for handling remove button clicked.
        """
        idx_list = self.ui.identifierList.selectedIndexes()
        rows_to_remove = [idx.row() for idx in idx_list]
        # Reverse sort the rows to remove, so we're not affected
        # by row index changes.
        rows_to_remove.sort(reverse=True)
        # Check if 
        for row in rows_to_remove:
            self._model.removeRow(row)

    def _handle_select_change(self, selected: QItemSelection, deselected: QItemSelection):
        """Private method for handling selection changed. Determines whether the Remove button is enabled.

        Args:
            selected (QItemSelection): Items selected.
            deselected (QItemSelection): Items deselected.
        """
        has_more_than_one_id = self._model.rowCount() > 1
        # Do not let user select and delete last ID.
        self.ui.btnDelete.setEnabled(len(selected) > 0 and has_more_than_one_id)
