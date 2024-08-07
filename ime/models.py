"""
models.py - Instrument Data Wizard dataclass models.
"""
# pylint: skip-file
import logging
import os
from typing import List, Dict, Any, Optional, Sequence, Type, TypeAlias
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
import yaml
from yaml.loader import Loader
from yaml import MappingNode, Dumper, FullLoader, Loader, Node, ScalarNode, UnsafeLoader
import logging
from pathlib import Path
from datetime import datetime
from ime.utils import st_dev
from ime.yaml_helpers import initialise_yaml_helpers

from ime.blueprints.custom_data_types import Username

class YAMLDataclass(yaml.YAMLObject):
    """A metaclass for dataclass objects to be serialised and deserialised by pyyaml."""

    @classmethod
    def from_yaml(cls: Type["YAMLDataclass"], loader: Loader, node: MappingNode) -> Any:
        """
        Convert a representation node to a Python object,
        calling __init__ to create a new object.

        We're using dataclasses to create an __init__ method
        which sets default values for fields not present in YAML document.
        By default, YAMLObject does not call __init__, so yaml.safe_load throws an exception
        on documents that don't have all required fields. (see https://github.com/yaml/pyyaml/issues/510,
        https://stackoverflow.com/questions/13331222/yaml-does-not-call-the-constructor)
        So we override the from_yaml method here to call __init__ (see
        https://stackoverflow.com/questions/7224033/default-constructor-parameters-in-pyyaml)
        """
        fields = loader.construct_mapping(node)
        return cls(**fields)

    def __getstate__(self) -> dict[str, Any]:
        """Override method for pyyaml. Returns a dictionary of key and value
        that should be serialised by yaml. Fields which have repr=False will not
        be included.
        See https://github.com/yaml/pyyaml/issues/612 for explanation on __getstate__.

        Returns:
            dict[str, Any]: A dictionary of key and values to be serialised in this class.
        """
        assert is_dataclass(self)
        return {
            field.name: getattr(self, field.name) 
            for field in fields(self) 
            if field.repr is True # Only include repr=True fields
        }

@dataclass
class UserACL(YAMLDataclass):
    """Model to define user access control. This differs from the group
    access control in that it validates the username against a known regex.
    """
    yaml_tag = "!UserACL"
    yaml_loader = yaml.SafeLoader
    user: Username = field(default=Username(), metadata={"label": "Username"})
    is_owner: bool = field(default=False, metadata={"label": "Is owner?"})
    can_download: bool = field(default=False, metadata={"label": "Can download?"})
    see_sensitive: bool = field(default=False, metadata={"label": "See sensitive?"})

@dataclass
class GroupACL(YAMLDataclass):
    """Model to define group access control."""
    yaml_tag = "!GroupACL"
    yaml_loader = yaml.SafeLoader
    group: str = field(default="", metadata={"label": "Group ID"})
    is_owner: bool = field(default=False, metadata={"label": "Is owner?"})
    can_download: bool = field(default=False, metadata={"label": "Can download?"})
    see_sensitive: bool = field(default=False, metadata={"label": "See sensitive?"})

@dataclass
class IAccessControl:
    """
    A class representing fields related to access
    control.
    When set to None, the fields represent that they are inheriting
    access control fields from the Project, Experiment or Dataset higher up
    in the hierarchy.
    """
    users: Optional[List[UserACL]] = None
    groups: Optional[List[GroupACL]] = None

class IIdentifiers:
    """An abstract class for methods working with identifiers,
    with default implementations. Specific MyTardis objects may
    override with specific constraints, for example to enforce
    uniqueness.
    """
    identifiers: Optional[List[str]]

    def __init__(self, identifiers: Optional[List[str]]) -> None:
        self.identifiers = identifiers
    
    def first(self) -> str:
        """Returns the first identifier in the list, if any.
        Otherwise return an empty string.

        Returns:
            str: The value of the ID.
        """
        if (self.identifiers is not None and 
            len(self.identifiers) > 0):
            return self.identifiers[0]
        else:
            return ""

    def has(self, ids: str | List[str]) -> bool:
        """Returns whether this object has identifier `ids`_ .
        If `ids`_ is a list, then returns whether this object has any
        identifier matching any in `ids`_

        Args:
            ids (str | List[str]): The id or list of ids to match

        Returns:
            bool: Whether any identifiers match.
        """
        if self.identifiers is None:
            return False
        elif type(ids) is str:
            return ids in self.identifiers
        else:
            # If we are comparing with a list of ids,
            # create sets with each list then get the
            # intersection of the sets. If there are none,
            # then we don't have any of the identifiers.
            id_set = set(self.identifiers or [])
            compare_set = set(ids)
            intersection = id_set & compare_set
            return len(intersection) > 0

    def add(self, value: str) -> bool:
        """Adds an identifier to the list. Classes
        inheriting may override with custom behaviour.

        Args:
            value (str): The new ID to add.
        """
        if self.identifiers is None:
            # Create the identifiers list with the new value.
            self.identifiers = [value]
            return True
        elif value not in self.identifiers:
            # If the value is not in the identifiers list,
            # then add to list.
            self.identifiers.append(value)
            return True
        else:
            # If the id is already in the list,
            # then don't do anything.
            return False

    def update(self, old_id: str, id: str) -> bool:
        """Method for updating an identifier. Classes
        inheriting may override with custom behaviour.

        Args:
            id (str): The new ID.
            old_id (str): The old ID to be replaced.
        """
        assert self.identifiers is not None
        idx = self.identifiers.index(old_id)
        self.identifiers[idx] = id
        return True

    def delete(self, id_to_delete: str) -> bool:
        """Method for deleting an identifier. Classes
        inheriting may override with custom behaviour.

        Args:
            id_to_delete (str): The ID to delete.
        """
        assert self.identifiers is not None
        self.identifiers.remove(id_to_delete)
        return True

class DataClassification(Enum):
    """An enumerator for data classification.
    Gaps have been left deliberately in the enumeration to allow for intermediate
    classifications of data that may arise. The larger the integer that the classification
    resolves to, the less sensitive the data is.
    """
    RESTRICTED = 1
    SENSITIVE = 25
    INTERNAL = 100
    PUBLIC = 100

@dataclass
class IDataClassification:
    """
    Common interface for MyTardis models with data classification labels.
    """
    data_classification: Optional[DataClassification] = None

class DataStatus(Enum):
    """An enumerator for data status.
    Gaps have been left deliberately in the enumeration to allow for intermediate
    status of data that may arise.
    """
    READY_FOR_INGESTION = 1
    INGESTED = 5

@dataclass
class IDataStatus:
    """
    Common interface for MyTardis models with data statud labels.
    """
    data_status: Optional[DataStatus] = None

@dataclass
class Project(
    YAMLDataclass, IAccessControl, IDataClassification, IDataStatus
):
    """
    A class representing MyTardis Project objects.

    Attributes:
        name (str): The name of the project.
        description (str): A brief description of the project.
        identifiers (List[str]): A list of identifiers for the project.
        data_classification (DataClassification): The data classification of the project.
        principal_investigator (str): The name of the principal investigator for the project.
    """
    yaml_tag = "!Project"
    yaml_loader = yaml.SafeLoader
    description: str = ""
    name: str = ""
    principal_investigator: Username = field(
        default=Username(), metadata={"label": "Username"}
    )
    identifiers: list[str] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    object_schema: str = "" # MTUrl in ingestion script
    # fields to add for updated data status
    created_by: Optional[str] = None
    institution: Optional[List[str]] = None
    start_time: Optional[datetime | str] = None
    end_time: Optional[datetime | str] = None
    embargo_until: Optional[datetime | str] = None
    delete_in_days: int = -1
    archive_in_days: int = 365
    url: Optional[str] = None
    _store: Optional["IngestionMetadata"] = field(repr=False, default=None)

    def __post_init__(self) -> None:
        self.identifiers_delegate = ProjectIdentifiers(self)

class ProjectIdentifiers(IIdentifiers):
    """Project-specific methods related to identifiers."""
    def __init__(self, project: Project):
        self.project = project
        super().__init__(project.identifiers)

    def _is_unique(self, id: str) -> bool:
        """Private method to check whether an id is unique across all
        Projects in the store.

        Args:
            id (str): The ID to check

        Returns:
            bool: True if the identifier is unique, False if not.
        """
        assert self.project._store is not None
        for project in self.project._store.projects:
            # If the project has this ID, then it isn't unique.
            if project.identifiers_delegate.has(id):
                return False
        return True

    def add(self, value: str) -> bool:
        """Adds a new identifier after checking
        if it's unique. Returns True if successfully added,
        returns False if it's not unique.

        Args:
            value (str): The new identifier.

        Returns:
            bool: Whether adding was successful.
        """
        if not self._is_unique(value):
            # Check if the new ID is unique.
            return False
        return super().add(value)

    def update(self, old_id: str, id: str) -> bool:
        """Updates an existing identifier in this Project and
        all related Experiments in the store. Checks if the identifier
        is unique. Returns True if successful, False if not.

        Args:
            old_id (str): The ID to update
            id (str): The new ID.

        Returns:
            bool: True if successfully updated, False if not unique.
        """
        assert self.project._store is not None
        # Find all experiments and update their IDs.
        if not self._is_unique(id):
            # Check if the new ID is unique.
            return False
        for experiment in self.project._store.experiments:
            if old_id in experiment.projects:
                # Update the projects list with the new_id
                experiment.projects.remove(old_id)
                experiment.projects.append(id)

        return super().update(old_id, id)

    def delete(self, id_to_delete: str) -> bool:
        """Deletes an identifier in this Project,
        and updates identifiers in related objects to use
        an alternative identifier.
        Returns True if successfully deleted and updated, False if
        there are no other identifiers to use for related objects.

        Args:
            id_to_delete (str): The identifier to delete.

        Returns:
            bool: True if successfully deleted, False if unable
            to delete.
        """
        if self.identifiers is None:
            return False
        if len(self.identifiers) <= 1:
            return False
        super().delete(id_to_delete)
        new_id = self.first()
        assert self.project._store is not None
        for experiment in self.project._store.experiments:
            if id_to_delete in experiment.projects:
                # Replace id_to_delete with the new_id within projects list
                experiment.projects.remove(id_to_delete)
                experiment.projects.append(new_id)
        return True

@dataclass
class Experiment(
    YAMLDataclass, IAccessControl, IDataClassification, IDataStatus
):
    """
    A class representing MyTardis Experiment objects.
    """
    yaml_tag = "!Experiment"
    yaml_loader = yaml.SafeLoader
    title: str = ""
    projects: List[str] = field(default_factory=list)
    description: str = ""
    identifiers: list[str] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    object_schema: str = "" # MTUrl in ingestion script
    # fields to add for updated data status
    institution_name: Optional[str] = None
    created_by: Optional[str] = None
    url: Optional[str] = None # MTUrl in ingestion script
    locked: bool = False
    start_time: Optional[datetime | str] = None
    end_time: Optional[datetime | str] = None
    created_time: Optional[datetime | str] = None
    update_time: Optional[datetime | str] = None
    embargo_until: Optional[datetime | str] = None
    _store: Optional["IngestionMetadata"] = field(repr=False, default=None)

    def __post_init__(self) -> None:
        self.identifiers_delegate = ExperimentIdentifiers(self)

class ExperimentIdentifiers(IIdentifiers):
    """Experiment-specific methods related to identifiers."""
    def __init__(self, experiment: Experiment):
        self.experiment = experiment
        super().__init__(experiment.identifiers)

    def _is_unique(self, id: str) -> bool:
        """Private method to check whether an id is unique across all
        Projects in the store.

        Args:
            id (str): The ID to check

        Returns:
            bool: True if the identifier is unique, False if not.
        """
        assert self.experiment._store is not None
        for experiment in self.experiment._store.experiments:
            # If the experiment has this ID, then it isn't unique.
            if experiment.identifiers_delegate.has(id):
                return False
        return True

    def add(self, value: str) -> bool:
        """Adds a new identifier after checking
        if it's unique. Returns True if successfully added,
        returns False if it's not unique.

        Args:
            value (str): The new identifier.

        Returns:
            bool: Whether adding was successful.
        """
        if not self._is_unique(value):
            return False
        return super().add(value)

    def update(self, old_id: str, id: str) -> bool:
        """Updates an existing identifier in this Experiment and
        all related Datasets in the store. Checks if the identifier
        is unique. Returns True if successful, False if not.

        Args:
            old_id (str): The ID to update
            id (str): The new ID.

        Returns:
            bool: True if successfully updated, False if not unique.
        """
        assert self.experiment._store is not None
        # Find all datasets and update their IDs.
        if not self._is_unique(id):
            # Check if the new ID is unique.
            return False
        for dataset in self.experiment._store.datasets:
            if old_id in dataset.experiments:
                dataset.experiments.remove(old_id)
                dataset.experiments.append(id)
        return super().update(old_id, id)

    def delete(self, id_to_delete: str) -> bool:
        """Deletes an identifier in this Experiment,
        and updates identifiers in related Datasets to use
        an alternative identifier.
        Returns True if successfully deleted and updated, False if
        there are no other identifiers to use for related objects.

        Args:
            id_to_delete (str): The identifier to delete.

        Returns:
            bool: True if successfully deleted, False if unable
            to delete.
        """
        if self.identifiers is None:
            return False
        if len(self.identifiers) <= 1:
            return False
        super().delete(id_to_delete)
        new_id = self.first()
        assert self.experiment._store is not None
        for dataset in self.experiment._store.datasets:
            if id_to_delete in dataset.experiments:
                dataset.experiments.remove(id_to_delete)
                dataset.experiments.append(new_id)
        return True

@dataclass
class Dataset(
    YAMLDataclass, IAccessControl, IDataClassification, IDataStatus
):
    """
    A class representing MyTardis Dataset objects.
    """
    yaml_tag = "!Dataset"
    yaml_loader = yaml.SafeLoader
    description: str = ""
    experiments: List[str] = field(default_factory=list)
    instrument: str = ""
    identifiers: list[str] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    object_schema: str = "" # MTUrl in ingestion script
    # fields to add for updated data status
    directory: Optional[Path] = None
    immutable: bool = False
    created_time: Optional[datetime | str] = None
    modified_time: Optional[datetime | str] = None
    _store: Optional["IngestionMetadata"] = field(repr=False, default=None)

    def __post_init__(self) -> None:
        """Dataclass lifecycle method that runs after an object is initialised. 
        This method initialises the identifier delegate class for this model."""
        self.identifiers_delegate = DatasetIdentifiers(self)

class DatasetIdentifiers(IIdentifiers):
    """Dataset-specific methods related to identifiers."""
    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        super().__init__(dataset.identifiers)

    def _is_unique(self, id: str) -> bool:
        """Private method to check whether an id is unique across all
        Projects in the store.

        Args:
            id (str): The ID to check

        Returns:
            bool: True if the identifier is unique, False if not.
        """
        assert self.dataset._store is not None
        for dataset in self.dataset._store.datasets:
            # If the experiment has this ID, then it isn't unique.
            if dataset.identifiers_delegate.has(id):
                return False
        return True

    def add(self, value: str) -> bool:
        """Adds a new identifier after checking
        if it's unique. Returns True if successfully added,
        returns False if it's not unique.

        Args:
            value (str): The new identifier.

        Returns:
            bool: Whether adding was successful.
        """
        if not self._is_unique(value):
            return False
        return super().add(value)

    def update(self, old_id: str, id: str) -> bool:
        """Updates an existing identifier in this Dataset and
        all related Datafiles in the store. Checks if the identifier
        is unique. Returns True if successful, False if not.

        Args:
            old_id (str): The ID to update
            id (str): The new ID.

        Returns:
            bool: True if successfully updated, False if not unique.
        """
        assert self.dataset._store is not None
        if not self._is_unique(id):
            return False
        # Find all experiments and update their IDs.
        for datafile in self.dataset._store.datafiles:
            if datafile.dataset == old_id:
                datafile.dataset = id
        return super().update(old_id, id)

    def delete(self, id_to_delete: str) -> bool:
        """Deletes an identifier in this Dataset,
        and updates identifiers in related Datafiles to use
        an alternative identifier.
        Returns True if successfully deleted and updated, False if
        there are no other identifiers to use for related objects.

        Args:
            id_to_delete (str): The identifier to delete.

        Returns:
            bool: True if successfully deleted, False if unable
            to delete.
        """
        if self.identifiers is None:
            return False
        if len(self.identifiers) <= 1:
            return False
        super().delete(id_to_delete)
        new_id = self.first()
        assert self.dataset._store is not None
        for datafile in self.dataset._store.datafiles:
            if datafile.dataset == id_to_delete:
                datafile.dataset = new_id
        return True

@dataclass
class Datafile(YAMLDataclass, IAccessControl, IDataStatus):
    """
    A class representing MyTardis Datafile objects.
    """
    yaml_tag = "!Datafile"
    yaml_loader = yaml.SafeLoader
    filename: str = ""
    directory: Optional[Path] = field(default_factory=Path)
    # This is for temporarily storing the absolute path,
    # required for generating relative path when saving.
    path_abs: Path = field(repr=False, default_factory=Path)
    size: float = 0
    md5sum: str = ""
    mimetype: str = ""
    dataset: str = ""
    metadata: Optional[Dict[str, Any]] = None
    object_schema: str = "" # MTUrl in ingestion script
    _store: Optional["IngestionMetadata"] = field(repr=False, default=None)

    def __getstate__(self) -> dict[str, Any]:
        """Override method for pyyaml's serialisation method,
        where we check if metadata is empty. If empty, we return
        None, because the ingestion script expects either a None
        or a dictionary with entries.

        Returns:
            dict[str, Any]: The state of the Datafile for serialisation.
        """
        file_state = super().__getstate__()
        if self.metadata is not None and len(self.metadata) == 0:
            # If metadata is an empty dict, then replace with a None.
            file_state["metadata"] = None
        return file_state

def Username_yaml_representer(dumper: Dumper, data: "Username") -> ScalarNode:
    """Function for representing this Username in YAML.
    When serialising to YAML that contains Username instances, you'll
    need to add this function as a representer.

    `yaml.add_representer(Username, Username.yaml_representer)`_

    Args:
        dumper (Dumper): The pyyaml dumper.
        data (Username): The Username to dump.

    Returns:
        ScalarNode: A serialised yaml Node.
    """
    return dumper.represent_scalar("!Username", str(data))

def Username_yaml_constructor(
    loader: Loader | FullLoader | UnsafeLoader, node: Node
) -> "Username":
    """Function for deserialising a node from YAML.
    When parsing YAML that contains Username instances, you'll
    need to add this function as a constructor.

    `yaml.add_constructor('!Username', Username.yaml_constructor)`_

    Args:
        loader (Loader): The pyyaml loader.
        node (ScalarNode): The node representing a Username.

    Returns:
        Username: A constructed username.
    """
    assert type(node) == ScalarNode
    value = loader.construct_scalar(node)
    return Username(value)

class DifferentDeviceException(Exception):
    """Exception that is thrown if ingestion metadata is
    saved in different device from the data."""
    pass

@dataclass
class IngestionMetadata:
    """
    A class representing a collection of metadata, with
    objects of different MyTardis types. It can be serialised
    to become a YAML file for ingestion into MyTardis.
    """
    # A list of objects of each type.
    projects: List[Project] = field(default_factory=list)
    experiments: List[Experiment] = field(default_factory=list)
    datasets: List[Dataset] = field(default_factory=list)
    datafiles: List[Datafile] = field(default_factory=list)
    # Ingestion metadata file location
    file_path: Optional[Path] = None

    @property
    def data_path(self) -> Optional[Path]:
        """Property for the effective workspace path for the data.
        Useful for checking if new data is stored in the same
        drive. If this IngestionMetadata was previously saved,
        the ingestion file path will be returned. Otherwise,
        this will return the first datafile's directory path.
        If there are no datafiles, a None will be returned.

        Returns:
            Optional[Path]: The workspace path for the data
        """
        if self.file_path is not None:
            return self.file_path.parent
        elif len(self.datafiles) > 0:
            return self.datafiles[0].path_abs
        else:
            return None

    def is_empty(self) -> bool:
        """Returns whether there are any projects, experiments,
        datasets and datafiles. 

        Returns:
            bool: True if there are, False if not.
        """
        return (
            len(self.projects) == 0
            and len(self.experiments) == 0
            and len(self.datasets) == 0
            and len(self.datafiles) == 0
        )

    def to_file(self, file_path: str) -> None:
        """Saves metadata to `file_path`_. Datafiles will be
        relative to the directory.

        Args:
            file_path (str): The file path to save the metadata file in.
        """
        path = Path(file_path)
        if self.data_path is not None:
            new_path_dev = st_dev(path.parent)
            data_dev = st_dev(self.data_path)
            if new_path_dev != data_dev:
                raise DifferentDeviceException()
        self._relativise_file_paths(path.parent)
        with open(path, "w") as file:
            file.write(self._to_yaml())
        self.file_path = path

    def _relativise_file_paths(self, relative_to_dir: Path) -> None:
        """Private method for modifying the Datafile paths to be relative
        to `relative_to_dir`_ . This is necessary when saving the file, so
        Datafile directory path is relative to the parent directory of
        the ingestion file.

        Args:
            relative_to_dir (Path): The directory that it would be relative to.
        """
        assert relative_to_dir.is_absolute()
        if self.file_path is not None:
            # If this file was previously saved,
            # then join the previous metadata file path with the relative path
            # in file.directory, then relativise to the new path.
            for file in self.datafiles:
                curr_path = self.file_path.parent.joinpath(file.directory) if file.directory is not None else self.file_path.parent
                new_path = curr_path.relative_to(relative_to_dir)
                file.directory = None if new_path == Path(".") else new_path
        else:
            # If this file is not previously saved, then use the absolute path for this
            # file.
            for file in self.datafiles:
                curr_path = file.path_abs.parent
                new_path = curr_path.relative_to(relative_to_dir)
                # Check if the new path is '.', set to '' if true
                file.directory = None if new_path == Path(".") else new_path
            
    def _to_yaml(self) -> str:
        """
        Returns a string of the YAML representation of the metadata.
        """
        concatenated: List[Any] = self.projects.copy()
        concatenated.extend(self.experiments)
        concatenated.extend(self.datasets)
        concatenated.extend(self.datafiles)
        yaml_file = yaml.dump_all(concatenated)
        return yaml_file

    def get_files_by_dataset(self, dataset: Dataset) -> List[Datafile]:
        """
        Returns datafiles that belong to a dataset.
        """
        all_files: List[Datafile] = []
        for file in self.datafiles:
            if not dataset.identifiers_delegate.has(file.dataset):
                continue
            # Concatenate list of fileinfo matching dataset
            # with current list
            all_files.append(file)
        return all_files

    def get_datasets_by_experiment(self, exp: Experiment) -> List[Dataset]:
        """
        Returns datasets that belong to a experiment.
        """
        all_datasets: List[Dataset] = []
        for dataset in self.datasets:
            # Check if any dataset experiment ids match experiment identifiers
            if not exp.identifiers_delegate.has(dataset.experiments):
                continue
            all_datasets.append(dataset)
        return all_datasets

    def get_experiments_by_project(self, proj: Project) -> List[Experiment]:
        """
        Returns experiments that belong to a project.
        """
        all_exps: List[Experiment] = []
        for exp in self.experiments:
            if not proj.identifiers_delegate.has(exp.projects):
                continue
            all_exps.append(exp)
        return all_exps

    @staticmethod
    def from_file(loc: str) -> "IngestionMetadata":
        """Factory method for importing a metadata file from path.

        Args:
            loc (Path): The location of the metadata file.

        Returns:
            IngestionMetadata: The imported metadata.
        """
        metadata = IngestionMetadata()
        metadata.file_path = Path(loc)
        with open(loc) as f:
            data_load = f.read()
        return IngestionMetadata._from_yaml(data_load, metadata)

    @staticmethod
    def _from_yaml(
        yaml_rep: str, metadata: Optional["IngestionMetadata"]
    ) -> "IngestionMetadata":
        """Returns a IngestionMetadata object by loading metadata from content of a YAML file.

        Parameters
        ----------
        yaml_rep : str
            The content of a YAML file. Note that this is the content, not the path of the file.
            The function does not read from a file for you, you have to pass in the file's content.
        """
        if metadata is None:
            metadata = IngestionMetadata()
        objects = yaml.safe_load_all(yaml_rep)
        # Iterate through all the objects,
        # sorting them into the right list
        # based on type.
        for obj in objects:
            if isinstance(obj, Project):
                obj._store = metadata
                metadata.projects.append(obj)
            elif isinstance(obj, Experiment):
                obj._store = metadata
                metadata.experiments.append(obj)
            elif isinstance(obj, Dataset):
                obj._store = metadata
                metadata.datasets.append(obj)
            elif isinstance(obj, Datafile):
                obj._store = metadata
                metadata.datafiles.append(obj)
            else:
                logging.warning(
                    "Encountered unknown object while reading YAML"
                    + ", ignored. Object was %s",
                    obj,
                )
        return metadata

MyTardisObject: TypeAlias = Project | Experiment | Dataset | Datafile

# Initialise the representers and constructors required for
# loading YAML elements.
initialise_yaml_helpers()
