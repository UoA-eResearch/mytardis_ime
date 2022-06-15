import yaml
from typing import List, Dict, Any
from dataclasses import dataclass, field

from yaml.loader import Loader
from yaml.nodes import MappingNode, ScalarNode, SequenceNode

class YAMLSerializable(yaml.YAMLObject):
    @classmethod
    def from_yaml(cls, loader: Loader, node) -> Any:
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
class IAccessControl():
    admin_groups: List[str] = field(default_factory=list)
    admin_users: List[str] = field(default_factory=list)
    read_groups: List[str] = field(default_factory=list)
    read_users: List[str] = field(default_factory=list)
    download_groups: List[str] = field(default_factory=list)
    download_users: List[str] = field(default_factory=list)
    sensitive_groups: List[str] = field(default_factory=list)
    sensitive_users: List[str] = field(default_factory=list)

@dataclass
class IMetadata():
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class Project(YAMLSerializable, IAccessControl, IMetadata):
    yaml_tag = u'!Project'
    yaml_loader = yaml.SafeLoader
    project_name: str = ""
    project_id: str = ""
    alternate_ids: List[str] = field(default_factory=list)
    description: str = ""
    lead_researcher: str = ""

@dataclass
class Experiment(YAMLSerializable, IAccessControl, IMetadata):
    yaml_tag = u'!Experiment'
    yaml_loader = yaml.SafeLoader
    experiment_name: str = ""
    project_id: str = ""
    experiment_id: str = ""
    alternate_ids: List[str] = field(default_factory=list)
    description: str = ""

@dataclass
class Dataset(YAMLSerializable, IAccessControl, IMetadata):
    yaml_tag = u'!Dataset'
    yaml_loader = yaml.SafeLoader
    dataset_name: str = ""
    experiment_id: List[str] = field(default_factory=list)
    dataset_id: str = ""
    instrument_id: str = ""

@dataclass
class FileInfo(YAMLSerializable, IAccessControl, IMetadata):
    yaml_tag = u'!FileInfo'
    yaml_loader = yaml.SafeLoader
    name: str = ""


@dataclass
class Datafile(YAMLSerializable):
    yaml_tag = u'!Datafile'
    yaml_loader = yaml.SafeLoader
    dataset_id: str = ""
    files: List[FileInfo] = field(default_factory=list)

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