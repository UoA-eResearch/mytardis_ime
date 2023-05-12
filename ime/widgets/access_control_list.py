from dataclasses import dataclass, field, fields
from typing import Generic, List, Optional, Type, TypeAlias, TypeVar, Union, cast
import typing

from PyQt5.QtCore import QModelIndex, QSignalBlocker, Qt, pyqtSignal
from ime.bindable import QObject
from ime.delegate import QVariant, TestEditorFactory
from ime.models import GroupACL, UserACL
from ime.qt_models import DataclassTableModel, PythonListModel
from ime.ui.ui_access_control_list import Ui_AccessControlList
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QMessageBox, QStyledItemDelegate, QWidget, QLineEdit, QItemEditorFactory

ACL_T = TypeVar('ACL_T', bound=Union[GroupACL, UserACL])

class AccessControlListTableModel(DataclassTableModel[ACL_T], Generic[ACL_T]):
    """
    A Qt Model specifically for AccessControlList.
    This class extends `DataclassTableModel`_ to render
    boolean fields as checkboxes, adds row inserting and
    deleting.
    """
    boolean_fields: list[str] = []

    def __init__(self, type: Type[ACL_T], parent:Optional[QObject]=None):
        super().__init__(type, parent)
        for field in fields(type):
            # Record the types.
            if field.type is bool:
                self.boolean_fields.append(field.name)

    # def _real_col_index(self, column: int) -> int:
    #     if column > 1:
    #         return column + 1
    #     elif column == 1:
    #         return -1
    #     else:
    #         return 0

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        """Override for QAbstractTableModel method.
        This enables showing section titles in `TableView`_.
        Titles are sourced from dataclass `metadata`_
        property. See `UserACL`_ and `GroupACL`_ for how
        they are specified.

        Args:
            section (int): Index of section.
            orientation (Qt.Orientation): Row or column.
            role (int, optional): Defaults to Qt.ItemDataRole.DisplayRole.

        Returns:
            typing.Any: The headerData value, title.
        """
        if (orientation == Qt.Orientation.Horizontal and
            role == Qt.ItemDataRole.DisplayRole):
            field_name = self.field_for_column(section)
            # Go through the type's fields to look for the section in question.
            for field in fields(self.type):
                if field.name == field_name:
                    # Look for a label property in the field's metadata.
                    # If it exists, return it as the section title.
                    metadata = field.metadata
                    if metadata["label"] is not None:
                        # Return the label as section title 
                        # if it exists.
                        return metadata["label"]
                    else:
                        # This field doesn't have a label.
                        break
        # If we don't find an appropriate label, go with default section name.
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """Override method for QAbstractTableModel. Check
        if this is a boolean field. If so return a flag that uses
        checkboxes instead. Otherwise fall back to 
        DataclassTableModel implementation.

        Args:
            index (QModelIndex): The index of the cell in question.

        Returns:
            Qt.ItemFlag: Appropriate item flags.
        """
        field = self.field_for_column(index.column())
        # Check if this is a boolean field.
        if field in self.boolean_fields:
            flags =  cast(Qt.ItemFlag, (
                    Qt.ItemFlag.ItemIsEnabled
                    | Qt.ItemFlag.ItemIsUserCheckable
            ))
            return flags
        else:
            return super().flags(index)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> typing.Any:
        field = self.field_for_column(index.column())
        if field in self.boolean_fields:
            if (role == Qt.ItemDataRole.CheckStateRole):
                d:bool = super().data(index)
                return Qt.CheckState.Checked if d else Qt.CheckState.Unchecked
        else:
            return super().data(index, role)

    def setData(self, index: QModelIndex, value: QVariant, role: int = Qt.ItemDataRole.DisplayRole) -> bool:
        field = self.field_for_column(index.column())
        if field in self.boolean_fields:
            if role == Qt.ItemDataRole.CheckStateRole:
                # Convert value to boolean
                val = value == Qt.CheckState.Checked
                return super().setData(index, val)
        return super().setData(index, value, role)

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(QModelIndex(), row, row+count-1)
        for i in range(row, row+count):
            # Create empty instances.
            self.instance_list.insert(i, self.type())
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row+count-1)
        for i in range(0, count):
            # Remove rows from largest index first
            # to avoid being affected by reassigned indices.
            idx = row+count-1-i
            self.instance_list.pop(idx)
        self.endRemoveRows()
        return True


    # def rowCount(self, parent=QModelIndex()) -> int:
    #     return super().rowCount() + 1


class AccessControlList(QWidget, Generic[ACL_T]):
    """A widget to display and edit access control lists.

    Attributes:
        _model (PythonListModel): A list model for the access control list.
        is_overriding_inheritance (bool): A flag to indicate whether the access controls are being overridden.
        override_inherited_toggled (pyqtSignal): A signal emitted when the override checkbox is toggled.
    """
    _model: AccessControlListTableModel[ACL_T]

    def __init__(self, parent = None):
        """Constructor for AccessControlList widget.

        Args:
            parent (QWidget): The parent widget (default is None).
        """ 
        super().__init__(parent)
        self.ui = Ui_AccessControlList()
        self.ui.setupUi(self)
        self.ui.btnAdd.clicked.connect(self._handle_insert_new)
        self.ui.btnDelete.clicked.connect(self._handle_remove)

    def data(self) -> List[ACL_T]:
        """Returns the currently displayed access control data.

        Returns:
            Union[OriginAccessControlData, DerivedAccessControlData]: The access control data
            being displayed.
        """
        return self._data

    def initialise_fields(self, type: Type[ACL_T]):
        """Initialises the AccessControlList with the type
        of data this list will display. `type`_ will be inspected
        for fields. `type`_ must be either `UserACL`_ or `GroupACL`_.

        Args:
            type (Type[ACL_T]): _description_
        """
        self._model = AccessControlListTableModel(type)
        self.ui.aclTable.setModel(self._model)
        self.ui.aclTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.aclTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    def set_data(self, value: List[ACL_T]):
        """
        Sets the access control data that will be displayed by the widget, and resets the widget interface
        using this data.
        
        Args:
            value (Union[OriginAccessControlData, DerivedAccessControlData]): _description_
        """
        self._data = value
        assert hasattr(self, '_model')
        self._model.set_instance_list(value)

    def set_disabled(self, disabled: bool) -> None:
        """Sets whether this access control list is disabled, and resets view to reflect. If enabled,
        new items can be added and existing items can be edited or deleted.
        If disabled, buttons are disabled.

        Args:
            disabled (bool): Whether this access control list is enabled.
        """
        self.ui.btnAdd.setDisabled(disabled)
        self.ui.btnDelete.setDisabled(disabled)
        self.ui.aclTable.setDisabled(disabled)

    def _handle_insert_new(self):
        """
        Handle the click of the "Add" button.

        Inserts a new row into the list model and sets the current index to the new row,
        allowing the user to edit it.
        """
        idx = self._model.rowCount()
        self._model.insertRow(idx)
        model_idx = self._model.index(idx, 0)
        self.ui.aclTable.setCurrentIndex(model_idx)
        self.ui.aclTable.edit(model_idx)

    def _handle_remove(self):
        """
        Handle the click of the "Remove" button.

        Removes the selected rows from the list model, in reverse order to avoid issues with row
        indices changing as rows are removed.
        """
        idx_list = self.ui.aclTable.selectedIndexes()
        rows_to_remove = [idx.row() for idx in idx_list]
        # Reverse sort the rows to remove, so we're not affected
        # by row index changes.
        rows_to_remove.sort(reverse=True)
        for row in rows_to_remove:
            self._model.removeRow(row)