from typing import List, Dict, Any, Optional, Type
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
import yaml
from yaml.loader import Loader
from yaml import MappingNode, Dumper, FullLoader, Loader, Node, ScalarNode, UnsafeLoader
import logging
import os.path
from ime.yaml_helpers import initialise_yaml_helpers

from pathlib import Path
from ime.yaml_helpers import initialise_yaml_helpers

from ime.blueprints.custom_data_types import Username

class YAMLDataclass(yaml.YAMLObject):
    """A metaclass for dataclass objects to be serialised and deserialised by pyyaml.
    """
    @classmethod
    def from_yaml(cls: Type, loader: Loader, node: MappingNode) -> Any:
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
    NOT_INGESTED = 1
    INGESTED = 5

@dataclass
class IDataStatus:
    """
    Common interface for MyTardis models with data statud labels.
    """
    data_status: Optional[DataStatus] = None

@dataclass
class IMetadata:
    """
    A class representing fields related to schema parameters.
    """
    # change to Optional[]
    metadata: Dict[str, Any] = field(default_factory=dict)
    object_schema: str = ""

@dataclass
class Project(YAMLDataclass, IAccessControl, IMetadata, IDataClassification, IDataStatus):
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
    name: str = ""
    description: str = ""
    project_id: str = ""
    alternate_ids: List[str] = field(default_factory=list)
    lead_researcher: str = ""
    principal_investigator: str = ""

@dataclass
class Experiment(YAMLDataclass, IAccessControl, IMetadata, IDataClassification, IDataStatus):
    """
    A class representing MyTardis Experiment objects.
    """

    yaml_tag = "!Experiment"
    yaml_loader = yaml.SafeLoader
    title: str = ""
    experiment_id: str = ""
    project_id: str = ""
    alternate_ids: List[str] = field(default_factory=list)
    description: str = ""



@dataclass
class Dataset(YAMLDataclass, IAccessControl, IMetadata, IDataClassification, IDataStatus):
    """
    A class representing MyTardis Dataset objects.
    """

    yaml_tag = "!Dataset"
    yaml_loader = yaml.SafeLoader
    dataset_name: str = ""
    description: str = ""
    dataset_id: str = ""
    experiment_id: List[str] = field(default_factory=list)
    instrument_id: str = ""
    instrument: str = ""
    experiments: List[str] = field(default_factory=list)


@dataclass
class Datafile(YAMLDataclass, IAccessControl, IMetadata, IDataStatus):
    """
    A class representing MyTardis Datafile objects.
    """
    yaml_tag = "!Datafile"
    yaml_loader = yaml.SafeLoader
    filename: str = ""
    directory: Path = field(default_factory=Path)
    # This is for temporarily storing the absolute path,
    # required for generating relative path when saving.
    path_abs: Path = field(repr=False, default_factory=Path)
    size: float = 0
    md5sum: str = ""
    mimetype: str = ""
    dataset: str = ""
    dataset_id: str = ""


def Username_yaml_representer(dumper: Dumper, data: 'Username') -> ScalarNode:
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
    return dumper.represent_scalar(u"!Username", str(data))

def Username_yaml_constructor(loader: Loader | FullLoader | UnsafeLoader, node: Node) -> 'Username':
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

    def is_empty(self) -> bool:
        return (len(self.projects) == 0 and
            len(self.experiments) == 0 and
            len(self.datasets) == 0 and
            len(self.datafiles) == 0
        )

    def to_file(self, file_path: str):
        """Saves metadata to `file_path`_. Datafiles will be
        relative to the directory.

        Args:
            file_path (str): The file path to save the metadata file in.
        """
        path = Path(file_path)
        with open(path, 'w') as file:
            self._relativise_file_paths(path.parent)
            file.write(self._to_yaml())
        self.file_path = path

    def _relativise_file_paths(self, relative_to_dir: Path) -> None:
        """Private method for changing the Datafile paths to be relative
        to `relative_to_dir`_ . This is necessary before saving. 

        Args:
            relative_to_dir (Path): The directory that it would be relative to.
        """
        assert relative_to_dir.is_absolute
        if self.file_path is not None:
            # If this was deserialised from a previously saved metadata file,
            # then join the previous metadata file path with the relative path
            # in file.directory, then relativise to the new path.
            for file in self.datafiles:
                curr_path = self.file_path.parent.joinpath(file.directory)
                new_path = Path(os.path.relpath(curr_path, relative_to_dir))
                file.directory = new_path
        else:
            # If this file is not previously saved, then use the absolute path for this
            # file.
            for file in self.datafiles:
                curr_path = file.path_abs.parent
                file.directory = Path(os.path.relpath(curr_path, relative_to_dir))

    def _to_yaml(self):
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
        id = dataset.dataset_id
        all_files: List[Datafile] = []
        for file in self.datafiles:
            if not file.dataset_id == id:
                continue
            # Concatenate list of fileinfo matching dataset
            # with current list
            all_files.append(file)
        return all_files

    def get_datasets_by_experiment(self, exp: Experiment) -> List[Dataset]:
        """
        Returns datasets that belong to a experiment.
        """
        id = exp.experiment_id
        all_datasets: List[Dataset] = []
        for dataset in self.datasets:
            if id not in dataset.experiment_id:
                continue
            all_datasets.append(dataset)
        return all_datasets
    
    def get_experiments_by_project(self, proj: Project) -> List[Experiment]:
        """
        Returns experiments that belong to a project.
        """
        id = proj.project_id
        all_exps: List[Experiment] = []
        for exp in self.experiments:
            if not exp.project_id == id:
                continue
            all_exps.append(exp)
        return all_exps

    @staticmethod
    def from_file(loc: str) -> 'IngestionMetadata':
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
    def _from_yaml(yaml_rep: str, metadata: Optional['IngestionMetadata']):
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
                metadata.projects.append(obj)
            elif isinstance(obj, Experiment):
                metadata.experiments.append(obj)
            elif isinstance(obj, Dataset):
                metadata.datasets.append(obj)
            elif isinstance(obj, Datafile):
                metadata.datafiles.append(obj)
            else:
                logging.warning(
                    "Encountered unknown object while reading YAML"
                    + ", ignored. Object was %s",
                    obj,
                )
        return metadata

# Initialise the representers and constructors required for
# loading YAML elements.
initialise_yaml_helpers()
