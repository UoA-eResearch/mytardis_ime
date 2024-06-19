import typing
from dataclasses import fields
from typing import Any, Generic, List, Optional, Type, TypeVar, Union, cast

from PySide6.QtCore import QItemSelection, QModelIndex, QObject, Qt
from PySide6.QtWidgets import QAbstractItemView, QApplication, QHeaderView, QWidget

from ime.models import GroupACL, UserACL
from ime.qt_models import DataclassTableModel, DataclassTableProxy
from ime.ui.ui_access_control_list import Ui_AccessControlList
from ime.widgets.qt_styles import CenteredCheckboxInViewItemStyle

ACL_T = TypeVar("ACL_T", bound=Union[GroupACL, UserACL])


class AccessControlListTableProxy(DataclassTableProxy[ACL_T], Generic[ACL_T]):
    """
    A Qt Proxy Model specifically for AccessControlList.
    This class extends `DataclassTableProxy`_ to render
    boolean fields as checkboxes, adds row inserting and
    deleting.
    """

    boolean_fields: list[str]

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.boolean_fields = []

    # Overrides for Qt Model methods follow.

    def setSourceModel(self, sourceModel: DataclassTableModel[ACL_T]) -> None:
        """Sets the source model for this Proxy Model. Any changes on this model
        will be synced with the source model and vice versa.

        Args:
            sourceModel (DataclassTableModel[ACL_T]): The source model.
        """
        super().setSourceModel(sourceModel)
        # Keep track of boolean fields.
        # This will be used to render them as checkboxes.
        for field in fields(sourceModel.type):
            if field.type is bool:
                self.boolean_fields.append(field.name)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> typing.Any:
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
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            sourceModel = self.sourceModel()
            field_name = sourceModel.field_for_column(section).name
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
        field = self.sourceModel().field_for_column(index.column()).name
        # Check if this is a boolean field.
        if field in self.boolean_fields:
            flags = cast(
                Qt.ItemFlag,
                (Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable),
            )
            return flags
        else:
            return super().flags(index)

    def data(
        self, index: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole
    ) -> typing.Any:
        """Return data for cell at `index`_. Override from the DataclassTableProxy
        function to render checkboxes for boolean fields.

        Args:
            index (QModelIndex): The index for the cell.
            role (Qt.ItemDataRole, optional): The Qt data role. Defaults to Qt.ItemDataRole.DisplayRole.

        Returns:
            typing.Any: The data for the cell.
        """
        field = self.sourceModel().field_for_column(index.column()).name
        if field in self.boolean_fields:
            # If the field is a boolean field, return a CheckState value instead
            # of boolean.
            if role == Qt.ItemDataRole.CheckStateRole:
                d: bool = self.sourceModel().data(index)
                return Qt.CheckState.Checked if d else Qt.CheckState.Unchecked
        else:
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                # Otherwise, return data as normal.
                # We assume that all data can be converted to string, since
                # this model will only deal with usernames and group IDs.
                return str(super().data(index, role))

    def setData(
        self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.DisplayRole
    ) -> bool:
        """Sets the data for cell at `index`_. Override to set boolean values
        based on check mark state.

        Args:
            index (QModelIndex): The index for the cell.
            value (QVariant): The new value.
            role (Qt.ItemDataRole, optional): The Qt data role. Defaults to Qt.ItemDataRole.DisplayRole.

        Returns:
            bool: Whether updating data was successful.
        """
        field = super().sourceModel().field_for_column(index.column())
        if field.name in self.boolean_fields and role == Qt.ItemDataRole.CheckStateRole:
            # Convert value to boolean
            val = value == Qt.CheckState.Checked.value
            return super().setData(index, val)
        else:
            # Deserialise back to original type from string.
            FieldType = field.type
            value = FieldType(value)
            return super().setData(index, value, role)

    def insertRows(self, row: int, count: int, parent=QModelIndex()) -> bool:
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
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        for i in range(row, row + count):
            # Create empty instances.
            sourceModel.instance_list.insert(i, sourceModel.type())
        self.endInsertRows()
        # Invalidate sorting and filtering so the changes show up.
        self.invalidate()
        return True

    def removeRows(self, row: int, count: int, parent=QModelIndex()) -> bool:
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
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        for i in range(0, count):
            # Remove rows from largest index first
            # to avoid being affected by reassigned indices.
            idx = row + count - 1 - i
            self.sourceModel().instance_list.pop(idx)
        self.endRemoveRows()
        # Invalidate sorting and filtering so the changes show up.
        self.invalidate()
        return True


class AccessControlList(QWidget, Generic[ACL_T]):
    """A widget to display and edit access control lists."""

    _model: AccessControlListTableProxy[ACL_T]

    def __init__(self, parent=None) -> None:
        """Constructor for AccessControlList widget.

        Args:
            parent (QWidget): The parent widget (default is None).
        """
        super().__init__(parent)
        self.ui = Ui_AccessControlList()
        self.ui.setupUi(self)
        self.ui.btnAdd.clicked.connect(self._handle_insert_new)
        self.ui.btnDelete.clicked.connect(self._handle_remove)
        # Disable delete button by default.
        self.ui.btnDelete.setDisabled(True)
        # Initialise styling for centering checkboxes
        aclTable = self.ui.aclTable
        check_style = CenteredCheckboxInViewItemStyle(QApplication.style().name())
        check_style.setParent(aclTable)
        aclTable.setStyle(check_style)

    def set_model(self, model: DataclassTableModel[ACL_T]) -> None:
        """Sets the DataclassTableModel this list will display,
        resets the interface with data. Any changes to the UserACL
        or GroupACL to display will come through the Model's
        signals.

        Args:
            type (Type[ACL_T]): _description_
        """
        self._model = AccessControlListTableProxy()
        self._model.setSourceModel(model)
        self.ui.aclTable.setModel(self._model)
        self.ui.aclTable.selectionModel().selectionChanged.connect(
            self._handle_select_change
        )
        # For name column, stretch.
        self.ui.aclTable.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        for i in range(1, model.columnCount()):
            # For columns other than name, resize to fit
            # the whole header name.
            self.ui.aclTable.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents
            )
        self.ui.aclTable.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

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

    def _handle_insert_new(self) -> None:
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

    def _handle_remove(self) -> None:
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

    def _handle_select_change(
        self, selected: QItemSelection, deselected: QItemSelection
    ) -> None:
        """Handler method for changes to which access control items are selected.

        Args:
            selected (QItemSelection): Selected items
            deselected (QItemSelection): Deselected items
        """
        self.ui.btnDelete.setEnabled(len(selected) > 0)
