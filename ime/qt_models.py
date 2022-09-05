from typing import Callable, Generic, List, TypeVar, Type
import typing
from PyQt5.QtCore import (
    QAbstractListModel,
    QAbstractTableModel,
    QModelIndex,
    QObject,
    QSortFilterProxyModel,
)

from .models import (
    Dataset,
    Experiment,
    IngestionMetadata,
    Project,
)
from dataclasses import fields
from PyQt5.QtCore import Qt

T = TypeVar("T")

class IngestionMetadataModel:
    def __init__(self, metadata = IngestionMetadata()):
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
        proxy.set_filter_by_instance(lambda exp: exp.project_id == id)
        return proxy

    def datasets_for_experiment(self, experiment: Experiment):
        id = experiment.experiment_id
        proxy = DataclassTableProxy(Dataset)
        proxy.setSourceModel(self.datasets)
        # Since the experiment_id field is a list, we add
        # a filter function to go through the list.
        proxy.set_filter_by_instance(lambda dataset: (id in dataset.experiment_id))
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

    def read_only_proxy(self, fields: List[str] = []):
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
    def rowCount(self, parent=QModelIndex()) -> int:
        if not parent.isValid():
            return len(self.instance_list)
        else:
            return 0  # TODO Implement retrieving nested data

    def columnCount(self, parent=QModelIndex()) -> int:
        if not parent.isValid():
            return len(self.fields)
        return 0  # TODO Implement retrieving nested data

    def setData(
        self,
        index: QModelIndex,
        value: typing.Any,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> bool:
        experiment = self.instance_list[index.row()]
        field_name = self.fields[index.column()]
        setattr(experiment, field_name, value)
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = (
            Qt.ItemFlag.ItemIsEditable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
        )
        return typing.cast(Qt.ItemFlags, flags)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> typing.Any:
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.fields[section]

    def data(
        self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            experiment = self.instance_list[index.row()]
            field = getattr(experiment, self.fields[index.column()])
            return field


class DataclassTableProxy(QSortFilterProxyModel, Generic[T]):
    read_only: bool = False
    show_fields: List[str] = []

    def __init__(self, type: Type[T], parent: typing.Optional[QObject] = None) -> None:
        self.type = type
        super().__init__(parent)

    def set_show_fields(self, show_fields: List[str]):
        self.show_fields = show_fields

    def set_read_only(self, read_only: bool):
        self.read_only = read_only

    def set_filter_by_instance(self, predicate: Callable[[T], bool]):
        """
        Sets a custom filter function for situations where the default
        fixed string and regexp filters are not adequate.
        predicate should take source_row index and source_parent, a QModelIndex,
        and return True or False of whether it should be included.
        """
        self.beginInsertColumns
        self.filter_by_instance = predicate

    def instance(self, row: int) -> T:
        source_row = self.mapToSource(self.index(row,0)).row()
        return self.sourceModel().instance(source_row)

    def setSourceModel(self, sourceModel: DataclassTableModel[T]) -> None:
        if not isinstance(sourceModel, DataclassTableModel):
            raise ValueError("You must use MyTaridsObjectModel as source model.")
        return super().setSourceModel(sourceModel)

    def sourceModel(self) -> DataclassTableModel[T]:
        return typing.cast(DataclassTableModel, super().sourceModel())

    def filterAcceptsColumn(
        self, source_column: int, source_parent: QModelIndex
    ) -> bool:
        if len(self.show_fields) == 0:
            # If no restrictions on what fields to show, return true for all columns.
            return True
        return self.sourceModel().field_for_column(source_column) in self.show_fields

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        if not hasattr(self, "custom_filter"):
            return super().filterAcceptsRow(source_row, source_parent)
        instance = self.sourceModel().instance(source_row)
        return self.filter_by_instance(instance)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if not self.read_only:
            flags |= Qt.ItemFlag.ItemIsEditable
        return typing.cast(Qt.ItemFlags, flags)
