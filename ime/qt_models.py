from typing import List, Union
import typing
from PyQt5.QtCore import QAbstractItemModel, QAbstractListModel, QAbstractTableModel, QIdentityProxyModel, QModelIndex, QObject
from .models import Dataset, Experiment, IAccessControl, IMetadata, IngestionMetadata, Project
from dataclasses import dataclass, fields
from PyQt5.QtCore import Qt

ACCESS_CONTROLS_FIELDS = [field.name for field in fields(IAccessControl)]
METADATA_FIELDS = [field.name for field in fields(IMetadata)]
# Make sure experiment fields come first
EXPERIMENT_FIELDS = [field.name for field in fields(Experiment) if field.name not in ACCESS_CONTROLS_FIELDS + METADATA_FIELDS] + ACCESS_CONTROLS_FIELDS + METADATA_FIELDS


class ViewOnlyDataModel(QIdentityProxyModel):
    def __init__(self, parent = None):
        super().__init__(parent)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        return typing.cast(Qt.ItemFlags, flags)

class ListModel(QAbstractListModel):
    def __init__(self, sourceList: List[str], parent = None):
        super().__init__(parent)
        self.list = sourceList

    def rowCount(self, parent = QModelIndex()) -> int:
        return len(self.list)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        return typing.cast(Qt.ItemFlags, flags)

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        self.list[index.row()] = value
        self.dataChanged.emit(index, index)
        return True

    def data(self, index: QModelIndex, role = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.list[index.row()]

    def headerData(self, section: int, orientation: Qt.Orientation, role = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return "hello"

    def insertRows(self, row: int, count: int, parent = QModelIndex()) -> bool:
        self.beginInsertRows(QModelIndex(), row, row+count-1)
        for i in range(row, row+count):
            self.list.insert(i, "")
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent = QModelIndex()) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row+count-1)
        for i in range(0, count):
            # Remove rows from largest index first
            # to avoid being affected by reassigned indices.
            idx = row+count-1-i
            self.list.pop(idx)
        self.endRemoveRows()
        return True

    def remove_value(self, val: str) -> bool:
        try:
            idx = self.list.index(val)
            self.beginRemoveRows(QModelIndex(), idx, idx)
            self.list.remove(val)
            self.endRemoveRows()
            return True
        except:
            return False

class IngestionMetadataModel():
    def __init__(self, metadata: IngestionMetadata):
        self.metadata = metadata
        


class MyTardisObjectModel(QAbstractTableModel):

    _keys = EXPERIMENT_FIELDS

    def column_for_field(self, field: str) -> int:
        for i, key in enumerate(self._keys):
            if key == field:
                return i
        return -1

    experiments: List[Union[Project, Experiment, Dataset]]

    def __init__(self, experiments: List[Union[Project, Experiment, Dataset]], parent=None):
        super().__init__(parent)
        self.experiments = experiments

    def rowCount(self, parent = QModelIndex()) -> int:
        if not parent.isValid():
            return len(self.experiments)
        else:
            return 0 # TODO Implement retrieving nested data

    def columnCount(self, parent = QModelIndex()) -> int:
        if not parent.isValid():
            return len(self._keys)
        return 0 # TODO Implement retrieving nested data

    def setData(self, index: QModelIndex, value: typing.Any, role: int = Qt.ItemDataRole.DisplayRole) -> bool:
        experiment = self.experiments[index.row()]
        field_name = self._keys[index.column()]
        setattr(experiment, field_name, value)
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        return typing.cast(Qt.ItemFlags, flags)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._keys[section]

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        experiment = self.experiments[index.row()]
        field = getattr(experiment, self._keys[index.column()])
        return field