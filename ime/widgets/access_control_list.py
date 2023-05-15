from dataclasses import fields
from typing import Generic, List, Optional, Type, TypeVar, Union, cast
import typing

from PyQt5.QtCore import QModelIndex, QVariant, Qt
from ime.bindable import QObject
from ime.models import GroupACL, UserACL
from ime.qt_models import DataclassTableModel, DataclassTableProxy
from ime.ui.ui_access_control_list import Ui_AccessControlList
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QWidget

ACL_T = TypeVar('ACL_T', bound=Union[GroupACL, UserACL])

class AccessControlListTableProxy(DataclassTableProxy[ACL_T], Generic[ACL_T]):
    """
    A Qt Proxy Model specifically for AccessControlList.
    This class extends `DataclassTableProxy`_ to render
    boolean fields as checkboxes, adds row inserting and
    deleting.
    """
    boolean_fields: list[str] = []

    def __init__(self, parent:Optional[QObject]=None):
        super().__init__(parent)

    # Overrides for Qt Model methods follow.

    def setSourceModel(self, sourceModel: DataclassTableModel[ACL_T]) -> None:
        super().setSourceModel(sourceModel)
        # Keep track of boolean fields.
        # This will be used to render them as checkboxes.
        for field in fields(sourceModel.type):
            if field.type is bool:
                self.boolean_fields.append(field.name)

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
            sourceModel = self.sourceModel()
            field_name = sourceModel.field_for_column(section)
            # Go through the type's fields to look for the section in question.
            for field in fields(sourceModel.type):
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
        if this is a boolean field. If so return the ItemFlag.ItemIsUserCheckable flag 
        which Qt Views will render as checkboxes instead. Otherwise fall back to 
        DataclassTableProxy implementation.

        Args:
            index (QModelIndex): The index of the cell in question.

        Returns:
            Qt.ItemFlag: Appropriate item flags.
        """
        field = self.sourceModel.field_for_column(index.column())
        # Check if this is a boolean field.
        if field in self.boolean_fields:
            flags =  cast(Qt.ItemFlag, (
                    Qt.ItemFlag.ItemIsEnabled
                    | Qt.ItemFlag.ItemIsUserCheckable
            ))
            return flags
        else:
            return super().flags(index)

    def data(self, index: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole
    ) -> typing.Any:
        """Return data for cell at `index`_. Override from the DataclassTableProxy
        function to render checkboxes for boolean fields.

        Args:
            index (QModelIndex): The index for the cell.
            role (Qt.ItemDataRole, optional): The Qt data role. Defaults to Qt.ItemDataRole.DisplayRole.

        Returns:
            typing.Any: The data for the cell.
        """
        field = self.sourceModel().field_for_column(index.column())
        if field in self.boolean_fields:
            # If the field is a boolean field, return a CheckState value instead
            # of boolean.
            if (role == Qt.ItemDataRole.CheckStateRole):
                d:bool = super().data(index)
                return Qt.CheckState.Checked if d else Qt.CheckState.Unchecked
        else:
            # Otherwise, return data as normal.
            return super().data(index, role)

    def setData(self, index: QModelIndex, value: QVariant, role: int = Qt.ItemDataRole.DisplayRole) -> bool:
        """Sets the data for cell at `index`_. Override to set boolean values
        based on check mark state.

        Args:
            index (QModelIndex): The index for the cell.
            value (QVariant): The new value.
            role (Qt.ItemDataRole, optional): The Qt data role. Defaults to Qt.ItemDataRole.DisplayRole.

        Returns:
            bool: Whether updating data was successful.
        """
        field = self.sourceModel().field_for_column(index.column())
        if field in self.boolean_fields:
            if role == Qt.ItemDataRole.CheckStateRole:
                # Convert value to boolean
                val = value == Qt.CheckState.Checked
                return super().setData(index, val)
        return super().setData(index, value, role)

    def insertRows(self, row: int, count: int, parent = QModelIndex()) -> bool:
        """Inserts row at an index. Creates a UserACL or GroupACL in the backing
        data model.

        Args:
            row (int): Row index.
            count (int): How many rows to create
            parent (QModelIndex, optional): The parent index, if this is a nested data model.
                Defaults to invalid QModelIndex.

        Returns:
            bool: Whether it was successful.
        """
        sourceModel = self.sourceModel()
        self.beginInsertRows(QModelIndex(), row, row+count-1)
        for i in range(row, row+count):
            # Create empty instances.
            sourceModel.instance_list.insert(i, sourceModel.type())
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent = QModelIndex()) -> bool:
        """Removes `count`_ instances starting at `row`_.

        Args:
            row (int): The index of the row
            count (int): Number of rows.
            parent (QModelIndex, optional): The parent index, 
                if this is a nested data model.
                Defaults to invalid QModelIndex.
        Returns:
            bool: True if successful, False if failed.
        """
        self.beginRemoveRows(QModelIndex(), row, row+count-1)
        for i in range(0, count):
            # Remove rows from largest index first
            # to avoid being affected by reassigned indices.
            idx = row+count-1-i
            self.sourceModel().instance_list.pop(idx)
        self.endRemoveRows()
        return True


    # def _real_col_index(self, column: int) -> int:
    #     if column > 1:
    #         return column + 1
    #     elif column == 1:
    #         return -1
    #     else:
    #         return 0

    # def rowCount(self, parent=QModelIndex()) -> int:
    #     return super().rowCount() + 1

class AccessControlList(QWidget, Generic[ACL_T]):
    """A widget to display and edit access control lists.

    Attributes:
        _model (PythonListModel): A list model for the access control list.
        is_overriding_inheritance (bool): A flag to indicate whether the access controls are being overridden.
        override_inherited_toggled (pyqtSignal): A signal emitted when the override checkbox is toggled.
    """
    data_model: DataclassTableModel[ACL_T]

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
        # Initialise the dataclass model for the list.
        self.data_model = DataclassTableModel(type)
        # Then create the view-specific table model.
        table_model = AccessControlListTableProxy()
        table_model.setSourceModel(self.data_model)
        self.ui.aclTable.setModel(table_model)
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
        assert hasattr(self, 'data_model')
        self.data_model.set_instance_list(value)

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