from abc import abstractmethod
from typing import Any, Callable, Generic, List, Optional, Union, TypeVar, Type
import typing
from PyQt5.QtCore import QAbstractItemModel, QAbstractListModel, QAbstractTableModel, QIdentityProxyModel, QModelIndex, QObject, QSortFilterProxyModel

from ime.models import FileInfo
from .models import Dataset, Datafile, Experiment, IAccessControl, IMetadata, IngestionMetadata, Project
from dataclasses import dataclass, fields
from PyQt5.QtCore import Qt

ACCESS_CONTROLS_FIELDS = [field.name for field in fields(IAccessControl)]
METADATA_FIELDS = [field.name for field in fields(IMetadata)]
# Make sure experiment fields come first
EXPERIMENT_FIELDS = [field.name for field in fields(Experiment) if field.name not in ACCESS_CONTROLS_FIELDS + METADATA_FIELDS] + ACCESS_CONTROLS_FIELDS + METADATA_FIELDS

T = TypeVar('T')

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
        self.projects = DataclassTableModel(Project)
        self.projects.set_instance_list(metadata.projects)
        self.experiments = DataclassTableModel(Experiment)
        self.experiments.set_instance_list(metadata.experiments)
        self.datasets = DataclassTableModel(Dataset)
        self.datasets.set_instance_list(metadata.datasets)
    
    def experiments_for_project(self, project: Project):
        id = project.project_id
        proxy = DataclassTableProxy(Experiment)
        proxy.setSourceModel(self.experiments)
        proxy.setFilterKeyColumn(self.experiments.column_for_field('project_id'))
        proxy.setFilterFixedString(id)
        return proxy

    def datasets_for_experiment(self, experiment: Experiment):
        id = experiment.experiment_id
        proxy = DataclassTableProxy(Dataset)
        proxy.setSourceModel(self.datasets)
        # Since the experiment_id field is a list, we add
        # a filter function to go through the list.
        proxy.set_custom_filter(lambda source_row: (
            id in self.datasets.instance(source_row).experiment_id
            )
        )
        return proxy

class DataclassTableModel(QAbstractTableModel, Generic[T]):

    instance_list: List[T]
    fields: List[str]

    def column_for_field(self, field: str) -> int:
        for i, key in enumerate(self.fields):
            if key == field:
                return i
        return -1

    def field_for_column(self, column: int) -> str:
        return self.fields[column]

    def get_read_only_proxy(self, fields: List[str] = []):
        """
        Return a read-only model of the whole model, mainly for
        displaying in a View.
        Optionally you may specify a list of fields to show in this table.
        """
        proxy = DataclassTableProxy(self.type)
        proxy.set_read_only(True)
        proxy.setSourceModel(self)
        proxy.set_show_fields(fields)
        return proxy

    def __init__(self, type: Type[T], parent=None):
        self.type = type
        self.fields = [field.name for field in fields(type)]
        super().__init__(parent)

    def instance(self, row: int) -> T:
        return self.instance_list[row]

    def set_instance_list(self, instance_list: List[T]):
            self.instance_list = instance_list

    # Implementations and overrides of QAbstractTableModel methods.
    def rowCount(self, parent = QModelIndex()) -> int:
        if not parent.isValid():
            return len(self.instance_list)
        else:
            return 0 # TODO Implement retrieving nested data

    def columnCount(self, parent = QModelIndex()) -> int:
        if not parent.isValid():
            return len(self.fields)
        return 0 # TODO Implement retrieving nested data

    def setData(self, index: QModelIndex, value: typing.Any, role: int = Qt.ItemDataRole.DisplayRole) -> bool:
        experiment = self.instance_list[index.row()]
        field_name = self.fields[index.column()]
        setattr(experiment, field_name, value)
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        return typing.cast(Qt.ItemFlags, flags)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.fields[section]

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            experiment = self.instance_list[index.row()]
            field = getattr(experiment, self.fields[index.column()])
            return field

class DataclassTableProxy(QSortFilterProxyModel, Generic[T]):
    read_only: bool = False
    show_fields: List[str] = []
    custom_filter: Callable

    def __init__(self, type: Type[T], parent: typing.Optional[QObject] = None) -> None:
        self.type = type
        super().__init__(parent)

    def set_show_fields(self, show_fields: List[str]):
        self.show_fields = show_fields

    def set_read_only(self, read_only: bool):
        self.read_only = read_only

    def set_custom_filter(self, predicate: Callable):
        """
        Sets a custom filter function for situations where the default
        fixed string and regexp filters are not adequate.
        predicate should take source_row index and source_parent, a QModelIndex, 
        and return True or False of whether it should be included.
        """
        self.custom_filter = predicate

    def setSourceModel(self, sourceModel: DataclassTableModel[T]) -> None:
        if not isinstance(sourceModel, DataclassTableModel):
            raise ValueError("You must use MyTaridsObjectModel as source model.")
        return super().setSourceModel(sourceModel)

    def sourceModel(self) -> DataclassTableModel[T]:
        return typing.cast(DataclassTableModel, super().sourceModel())

    def filterAcceptsColumn(self, source_column: int, source_parent: QModelIndex) -> bool:
        if len(self.show_fields) == 0:
            # If no restrictions on what fields to show, return true for all columns.
            return True
        return self.sourceModel().field_for_column(source_column) in self.show_fields

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        if not hasattr(self, 'custom_filter'):
            return super().filterAcceptsRow(source_row, source_parent)
        return self.custom_filter(source_row, source_parent)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if not self.read_only:
            flags |= Qt.ItemFlag.ItemIsEditable
        return typing.cast(Qt.ItemFlags, flags)
