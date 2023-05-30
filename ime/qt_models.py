"""
qt_models.py - Adaptor classes for Qt's Model/View architecture.
These classes connect the MyTardis object models in models.py
into Qt's Model View architecture, so they can be used by
Qt Tree/Table/ListView widgets and act as a single source of 
truth for data in the UI.
The clases are split into: DataclassTableModel and DataclassTableProxy
which implement/extend Qt model and proxy interfaces; and an IngestionMetadataModel
model which adapts IngestionMetadata from models.py for Qt, using the two other
models.
"""
from typing import Any, Callable, Generic, List, Optional, TypeVar, Type, cast
import typing
from PyQt5.QtCore import (
    QAbstractListModel,
    QAbstractTableModel,
    QModelIndex,
    QObject,
    QSortFilterProxyModel
)

from .models import (
    Dataset,
    Experiment,
    IngestionMetadata,
    Project,
)
from dataclasses import Field, fields
from PyQt5.QtCore import Qt

T = TypeVar("T")

class PythonListModel(QAbstractListModel):
    """A basic implementation of a Qt Model that updates a Python list.
    The built-in QStringListModel creates a separate list object, which
    means the original Python list doesn't get updated.
    """
    list: List[str]
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

    def setStringList(self, sourceList: List[str]) -> None:
        """Sets the source Python string list that will be updated by 
        this Model.

        Args:
            sourceList (List[str]): The backing Python string list.
        """
        self.beginResetModel()
        self.list = sourceList
        self.endResetModel()

    def remove_value(self, val: str) -> bool:
        """Remove a given value from the list, and send appropriate
        Qt Model signals to notify any views of the change.

        Args:
            val (str): The value to be removed.

        Returns:
            bool: Whether the removal was successful or not.
        """
        try:
            idx = self.list.index(val)
            self.beginRemoveRows(QModelIndex(), idx, idx)
            self.list.remove(val)
            self.endRemoveRows()
            return True
        except:
            return False

    # The following methods implement the QAbstractListModel interface.
    # Documentation about these methods can be found in:
    # https://doc.qt.io/qt-6/qabstractlistmodel.html

    def rowCount(self, parent = QModelIndex()) -> int:
        """Returns the number of rows in the model."""
        if not hasattr(self, 'list'):
            return 0
        return len(self.list)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """Returns the flags associated with the given index."""
        flags = Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        return typing.cast(Qt.ItemFlags, flags)

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        """Sets the data at the given index to the given value."""
        self.list[index.row()] = value
        self.dataChanged.emit(index, index)
        return True

    def data(self, index: QModelIndex, role = Qt.ItemDataRole.DisplayRole) -> typing.Any:
        """Returns the data stored under the given role for the item referred to by the index."""
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self.list[index.row()]

    def insertRows(self, row: int, count: int, parent = QModelIndex()) -> bool:
        """Inserts rows into the model."""
        self.beginInsertRows(QModelIndex(), row, row+count-1)
        for i in range(row, row+count):
            self.list.insert(i, "")
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent = QModelIndex()) -> bool:
        """Removes rows from the model."""
        self.beginRemoveRows(QModelIndex(), row, row+count-1)
        for i in range(0, count):
            # Remove rows from largest index first
            # to avoid being affected by reassigned indices.
            idx = row+count-1-i
            self.list.pop(idx)
        self.endRemoveRows()
        return True



class IngestionMetadataModel:
    """
    An adaptor class for IngestionMetadata from models.py.
    Wraps projects/experiments/datasets with DataclassTableModel
    so that they can be used for Qt Tree/Table/ListViews. You can
    also derive read-only or filtered versions of each model using
    DataclassTableProxy - see below.
    """
    def __init__(self, metadata = IngestionMetadata()) -> None:
        """
        Initializes an instance of the IngestionMetadataModel class.
        Args:
            metadata: An instance of the IngestionMetadata class from models.py. Defaults to an empty instance.
        """
        self.metadata = metadata
        self.projects = DataclassTableModel(Project)
        self.projects.set_instance_list(metadata.projects)
        self.experiments = DataclassTableModel(Experiment)
        self.experiments.set_instance_list(metadata.experiments)
        self.datasets = DataclassTableModel(Dataset)
        self.datasets.set_instance_list(metadata.datasets)

    def experiments_for_project(self, project: Project):
        """
        Returns a filtered data model of all Experiments that belong 
        to a Project in this model. 
        """
        proxy = self.experiments.proxy()
        proxy.set_filter_by_instance(lambda exp: 
            project.identifiers_delegate.has(cast(Experiment, exp).project_id)
        )
        return proxy

    def datasets_for_experiment(self, experiment: Experiment):
        """
        Returns a filtered data model of all Datasets that belong to an
        Experiment in this model.
        """
        proxy = self.datasets.proxy()
        # Since the experiment_id field is a list, we add
        # a filter function to go through the list.
        proxy.set_filter_by_instance(lambda dataset:
            experiment.identifiers_delegate.has(cast(Dataset, dataset).experiment_id)
        )
        return proxy
    
    def project_for_experiment(self, experiment: Experiment):
        """
        Returns a DataclassTableProxy of projects that have a given experiment as a part.
        :param experiment: An Experiment object.
        :return: A DataclassTableProxy of projects.
        """
        proxy = self.projects.proxy()
        proxy.set_filter_by_instance(lambda proj: 
            cast(Project, proj).identifiers_delegate.has(experiment.project_id)
        )
        return proxy

class DataclassTableModel(QAbstractTableModel, Generic[T]):
    """
    An Qt Model adaptor class for a Python list of dataclasses, implemented as a
    TableModel. Each row represents an "instance" of dataclass in the list, and each 
    column represents a "field" in the instance. 
    Field name and its column order are determined by the name and order of dataclasses 
    fields returned by the fields() function.
    To instantiate the class:
    ```
    object_list = [MyDataclass("hello"), MyDataclass("world!")] # construct the data list.

    model = DataclassTableModel(MyDataclass) # specify which class we're using

    model.set_instance_list(object_list) # add the data list into the model.
    ```
    """

    instance_list: List[T]
    fields: List[str]

    def column_for_field(self, field: str) -> int:
        """
        Given a field name, return its column index.
        """
        for i, key in enumerate(self.fields):
            if key == field:
                return i
        return -1

    def field_for_column(self, column: int) -> Field:
        """
        Given a column index, return the corresponding field name.
        """
        return fields(self.type)[column]

    def proxy(self, fields: List[str] = []):
        """
        Convenience function that returns a proxy model of the whole model, 
        useful for a filtered view or displaying in a View.
        Optionally you may specify a list of `fields` to show in this table. Fields will
        be ordered in the proxy model according to the order of the list.
        """
        instance_type = self.type
        proxy = DataclassTableProxy[instance_type]()
        proxy.setSourceModel(self)
        proxy.set_show_fields(fields)
        return proxy

    def __init__(self, type: Type[T], parent=None) -> None:
        """
        Instantiate DataclassTableModel. The `type` passed in will be
        inspected for its dataclass fields.
        """
        self.type = type
        self.instance_list = []
        self.fields = [field.name for field in fields(type)]
        super().__init__(parent)

    def instance(self, row: int) -> T:
        """
        Given the row index, return the instance of dataclass represented
        in that row.
        """
        return self.instance_list[row]

    def set_instance_list(self, instance_list: List[T]) -> None:
        """
        Set the backing dataclass list this model will represent. 
        """
        self.beginResetModel()
        self.instance_list = instance_list
        self.endResetModel()
    
    def add_extra_field(self, field_name: str) -> int:
        # TODO This will be useful for computed values like project/experiment/dataset size.
        # And perhaps the effective ACL users and groups?
        # compute_fn will be re-evaluated for an instance when any of its fields has changed.
        # If an external dependency of the function changes, the model needs to be notified, 
        # so compute_fn can be re-evaluated.
        # e.g.  DataclassTableModel.field_changed(row, fields)? But may be circular.
        raise NotImplementedError()

    def field_changed(self, row: int, field: str):
        # Notifies the model that this instance's field has changed.
        # A wrapper around dataChanged().
        raise NotImplementedError()

    # Implementations and overrides of QAbstractTableModel methods follow.
    # These methods are mainly for use by native Qt Views.
    def rowCount(self, parent=QModelIndex()) -> int:
        """
        Returns the number of rows in the model.

        Args:
            parent (QtCore.QModelIndex): The parent model index.

        Returns:
            int: The number of rows in the model.
        """
        return len(self.instance_list)

    def columnCount(self, parent=QModelIndex()) -> int:
        """
        Returns the number of columns in the model.

        Args:
            parent (QtCore.QModelIndex): The parent model index.

        Returns:
            int: The number of columns in the model.
        """
        if not parent.isValid():
            return len(self.fields)
        return 0  # TODO Implement retrieving nested data

    def setData(
        self,
        index: QModelIndex,
        value: typing.Any,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> bool:
        """
        Sets the data for the given model index and role.

        Args:
            index (QtCore.QModelIndex): The model index.
            value (typing.Any): The new value to set.
            role (QtCore.Qt.ItemDataRole): The data role.

        Returns:
            bool: True if the data was set successfully; otherwise, False.
        """
        experiment = self.instance_list[index.row()]
        field_name = self.fields[index.column()]
        setattr(experiment, field_name, value)
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """
        Returns the flags for the given model index.

        Args:
            index (QtCore.QModelIndex): The model index.

        Returns:
            QtCore.Qt.ItemFlag: The flags for the given model index.
        """
        flags = (
            Qt.ItemFlag.ItemIsEditable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsUserCheckable
        )
        return typing.cast(Qt.ItemFlag, flags)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> typing.Any:
        """
        Returns the header data for the given section, orientation, and role.

        Args:
            section (int): The section index.
            orientation (QtCore.Qt.Orientation): The header orientation.
            role (QtCore.Qt.ItemDataRole): The data role.

        Returns:
            typing.Any: The header data for the given section, orientation, and role.
        """
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.fields[section]
    def data(
        self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> typing.Any:
        """
        Returns the data for the given model index and role.

        Args:
            index (QtCore.QModelIndex): The model index.
            role (QtCore.Qt.ItemDataRole): The data role.

        Returns:
            typing.Any: The data for the given model index and role.
        """
        if (role == Qt.ItemDataRole.DisplayRole or
            role == Qt.ItemDataRole.EditRole):
            instance = self.instance_list[index.row()]
            field = getattr(instance, self.fields[index.column()])
            return field

class DataclassTableProxy(QSortFilterProxyModel, Generic[T]):
    """
    A class that extends the QSortFilterProxyModel with dataclass-specific and other
    utility functions.
    
    In Qt, a ProxyModel class is a copy of a Model that is synced up with the Model's
    changes. A Proxy can filter out some of the data or add different ways of displaying things. 
    A ProxyModel can be used in any Qt View in the same way as Models. They are useful for 
    showing the same data in different ways, for example a list view and a detail view.
    
    Usually, you create an instance using the DataclassTableModel.proxy() method.
    To directly instantiate the class:
    ```
    model = DataclassTableModel(MyDataclass) # create the source model.
    proxy = DataclassTableProxy[MyDataclass]() # create the proxy, with the same class type as the model.
    proxy.setSourceModel(model) # Add the model as source for the proxy.
    ```

    """
    read_only: bool = False
    show_fields: List[str] = []

    def __init__(self, parent: typing.Optional[QObject] = None) -> None:
        super().__init__(parent)

    def set_show_fields(self, show_fields: List[str]) -> None:
        """
        Given a list of field names, sets which dataclass fields should be 
        shown by the proxy model. If show_fields is an empty list, then all fields
        will be shown.
        """
        self.show_fields = show_fields

    def set_read_only(self, read_only: bool) -> None:
        """
        Sets whether the proxy model should use read-only flags. 
        This primarily affects native Qt View widgets, which shows an editing widget or
        a plain label for each item depending on the flags.
        """
        self.read_only = read_only

    def set_filter_by_instance(self, predicate: Callable[[T], bool]) -> None:
        """
        Applies a predicate (a function that takes an argument and returns
        True or False) to each dataclass instance in the model, and filter out
        instances that predicate returns False on. 
        predicate should take an instance of the dataclass T,
        and return True or False of whether it should be included.
        Note, if a predicate is set, then QSortFilterProxyModel's built-in filters
        (e.g. filterFixedString()) will not be applied even if set.
        """
        self.beginInsertColumns
        self.filter_by_instance = predicate

    def instance(self, row: int) -> T:
        """
        Given a row index in the Proxy Model, returns the dataclass instance
        represented by the row.
        """
        source_row = self.mapToSource(self.index(row,0)).row()
        return self.sourceModel().instance(source_row)

    # Implementations and overrides of QAbstractTableModel methods follow.
    # These methods are mainly for use by native Qt Views.
    def setSourceModel(self, sourceModel: DataclassTableModel[T]) -> None:
        # Ensure only DataclassTableModel is used as source models.
        """
        Overrides the `setSourceModel()` method of QSortFilterProxyModel to ensure
        that only DataclassTableModel instances are used as source models.

        Args:
            sourceModel (DataclassTableModel): The source model to be set.
        """
        return super().setSourceModel(sourceModel)

    def sourceModel(self) -> DataclassTableModel[T]:
        # Change the sourceModel function so that it gives richer type completion
        # in type checkers.
        """
        Overrides the `sourceModel()` method of QSortFilterProxyModel to give richer
        type completion in type checkers.
        """
        return typing.cast(DataclassTableModel, super().sourceModel())

    def filterAcceptsColumn(
        self, source_column: int, source_parent: QModelIndex
    ) -> bool:
        """
        Overrides the `filterAcceptsColumn()` method of QSortFilterProxyModel to filter
        columns of the source model.

        Args:
            source_column (int): The index of the source column to be filtered.
            source_parent (QModelIndex): The index of the source parent.

        Returns:
            bool: True if the column passes the filter; False otherwise.
        """
        if len(self.show_fields) == 0:
            # If no restrictions on what fields to show, return true for all columns.
            return True
        return self.sourceModel().field_for_column(source_column).name in self.show_fields

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        Overrides the `filterAcceptsRow()` method of QSortFilterProxyModel to filter
        rows of the source model.

        Args:
            source_row (int): The index of the source row to be filtered.
            source_parent (QModelIndex): The index of the source parent.

        Returns:
            bool: True if the row passes the filter; False otherwise.
        """
        if not hasattr(self, "filter_by_instance"):
            return super().filterAcceptsRow(source_row, source_parent)
        instance = self.sourceModel().instance(source_row)
        return self.filter_by_instance(instance)

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """
        Overrides the `flags()` method of QSortFilterProxyModel to set the flags for the
        model items.

        Args:
            index (QModelIndex): The index of the item.

        Returns:
            Qt.ItemFlag: The flags for the item.
        """
        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if not self.read_only:
            flags |= Qt.ItemFlag.ItemIsEditable
        return typing.cast(Qt.ItemFlag, flags)

    def columnCount(self, parent = QModelIndex()) -> int:
        """
        Return the number of columns in the model.

        Args:
            parent (QModelIndex, optional): Parent index. Defaults to QModelIndex().

        Returns:
            int: Number of columns in the model.
        """
        if len(self.show_fields) > 0:
            return len(self.show_fields)
        return super().columnCount(parent)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> typing.Any:
        """
        Return the data for the header specified by section, orientation and role.

        Args:
            section (int): Section number.
            orientation (Qt.Orientation): Header orientation.
            role (int, optional): Data role. Defaults to Qt.ItemDataRole.DisplayRole.

        Returns:
            typing.Any: The header data.
        """
        if (
            len(self.show_fields) > 0 and
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return self.show_fields[section]
        return super().headerData(section, orientation, role)

    def data(
        self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> typing.Any:
        """
        Return the data stored under the given role for the item referred to by the index.

        Args:
            index (QModelIndex): Index of the item.
            role (int, optional): Data role. Defaults to Qt.ItemDataRole.DisplayRole.

        Returns:
            typing.Any: The data stored under the given role for the item referred to by the index.
        """
        if (
            len(self.show_fields) > 0 and
            role == Qt.ItemDataRole.DisplayRole
        ):
            instance = self.instance(index.row())
            field = getattr(instance, self.show_fields[index.column()])
            return field
        return super().data(index, role)