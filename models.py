from typing import List, Dict, Any, Type
from dataclasses import dataclass, field
import yaml
from yaml.loader import Loader
from yaml.nodes import Node
import logging


class YAMLSerializable(yaml.YAMLObject):
    @classmethod
    def from_yaml(cls: Type, loader: Loader, node: Node) -> Any:
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


@dataclass
class IAccessControl:
    """
    A class representing fields related to ACL controls.
    """

    admin_groups: List[str] = field(default_factory=list)
    admin_users: List[str] = field(default_factory=list)
    read_groups: List[str] = field(default_factory=list)
    read_users: List[str] = field(default_factory=list)
    download_groups: List[str] = field(default_factory=list)
    download_users: List[str] = field(default_factory=list)
    sensitive_groups: List[str] = field(default_factory=list)
    sensitive_users: List[str] = field(default_factory=list)


@dataclass
class IMetadata:
    """
    A class representing fields related to schema parameters.
    """

    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class Project(YAMLSerializable, IAccessControl, IMetadata):
    """
    A class representing MyTardis Project objects.
    """

    yaml_tag = "!Project"
    yaml_loader = yaml.SafeLoader
    # yaml_dumper = yaml.SafeDumper
    project_name: str = ""
    project_id: str = ""
    alternate_ids: List[str] = field(default_factory=list)
    description: str = ""
    lead_researcher: str = ""


@dataclass
class Experiment(YAMLSerializable, IAccessControl, IMetadata):
    """
    A class representing MyTardis Experiment objects.
    """

    yaml_tag = "!Experiment"
    yaml_loader = yaml.SafeLoader
    # yaml_dumper = yaml.SafeDumper
    experiment_name: str = ""
    project_id: str = ""
    experiment_id: str = ""
    alternate_ids: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class Dataset(YAMLSerializable, IAccessControl, IMetadata):
    """
    A class representing MyTardis Dataset objects.
    """

    yaml_tag = "!Dataset"
    yaml_loader = yaml.SafeLoader
    # yaml_dumper = yaml.SafeDumper
    dataset_name: str = ""
    experiment_id: List[str] = field(default_factory=list)
    dataset_id: str = ""
    instrument_id: str = ""


@dataclass
class FileInfo(YAMLSerializable, IAccessControl, IMetadata):
    """
    A class representing MyTardis Datafile objects.
    """

    yaml_tag = "!FileInfo"
    # yaml_dumper = yaml.SafeDumper
    yaml_loader = yaml.SafeLoader
    name: str = ""


@dataclass
class Datafile(YAMLSerializable):
    """
    A class representing a set of MyTardis datafile objects.
    """

    yaml_tag = "!Datafile"
    yaml_loader = yaml.SafeLoader
    # yaml_dumper = yaml.SafeDumper
    dataset_id: str = ""
    files: List[FileInfo] = field(default_factory=list)


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

    def to_yaml(self):
        """
        Returns a string of the YAML representation of the metadata.
        """
        concatenated: List[Any] = self.projects
        concatenated.extend(self.experiments)
        concatenated.extend(self.datasets)
        concatenated.extend(self.datafiles)
        yaml_file = yaml.dump_all(concatenated)
        return yaml_file

    @staticmethod
    def from_yaml(yaml_rep: str):
        """Returns a IngestionMetadata object by loading metadata from content of a YAML file.

        Parameters
        ----------
        yaml_rep : str
            The content of a YAML file. Note that this is the content, not the path of the file.
            The function does not read from a file for you, you have to pass in the file's content.
        """
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


# # To use:
# dataset = Dataset()
# dataset.dataset_name = "Calibration 10 X"
# dataset.dataset_id = "2022-06-calibration-10-x"

# # To dump into YAML
# yaml.dump(dataset)

# # To dump multiple objects
# datafile = Datafile()
# datafile.dataset_id = "2022-06-calibration-10-x"
# output = [dataset, datafile]
# yaml.dump_all(output)

# # If not working with tags, strip them out and process as normal.
# import yaml
# from yaml.nodes import MappingNode, ScalarNode, SequenceNode
# def strip_unknown_tag_and_construct(loader, node):
#     node.tag = ""
#     # print(node)
#     if isinstance(node, ScalarNode):
#         return loader.construct_scalar(node)
#     if isinstance(node, SequenceNode):
#         return loader.construct_sequence(node)
#     if isinstance(node, MappingNode):
#         return loader.construct_mapping(node)
#     else:
#         return None

# yaml.SafeLoader.add_constructor(None, strip_unknown_tag_and_construct)
# with open('test/test.yaml') as f:
#     a = list(yaml.safe_load_all(f))
