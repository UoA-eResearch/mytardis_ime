"""YAML representers and constructors required for working with model data.
This is used by `ime.models`_ .
"""
from yaml import Dumper, FullLoader, Loader, Node, ScalarNode, UnsafeLoader
from pathlib import Path

import yaml
from ime.blueprints.custom_data_types import Username

def Path_yaml_representer(dumper: Dumper, data: Path) -> ScalarNode:
    """Function for representing this Path in YAML.
    When serialising to YAML that contains Path instances, you'll
    need to add this function as a representer. Because Path has
    multiple subclasses depending on platform, `add_multi_representer`_
    is required.

    `yaml.add_multi_representer(Path, Path_yaml_representer)`_
    
    Args:
        dumper (Dumper): The pyyaml dumper.
        data (Path): The Path to dump.

    Returns:
        ScalarNode: A serialised yaml Node.
    """
    return dumper.represent_scalar(u"!Path", str(data))

def Path_yaml_constructor(loader: Loader | FullLoader | UnsafeLoader, node: Node) -> Path:
    """Function for deserialising a node from YAML.
    When parsing YAML that contains Path instances, you'll
    need to add this function as a constructor.
    
    `yaml.add_constructor('!Path', Path_yaml_constructor)`_

    Args:
        loader (Loader): The pyyaml loader.
        node (ScalarNode): The node representing a Username.

    Returns:
        Path: A constructed path.
    """
    assert type(node) == ScalarNode
    value = loader.construct_scalar(node)
    assert type(value) is str
    return Path(value)

def Username_yaml_representer(dumper: Dumper, data: Username) -> ScalarNode:
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

def Username_yaml_constructor(loader: Loader | FullLoader | UnsafeLoader, node: Node) -> Username:

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

def initialise_yaml_helpers():
    """Initialises YAML constructor and representer required to parse
    and serialise MyTardis model data. This is called when the ime.models 
    module is loaded and do not need a separate call.
    """
    yaml.SafeLoader.add_constructor('!Username', Username_yaml_constructor)
    yaml.add_representer(Username, Username_yaml_representer)
    yaml.SafeLoader.add_constructor('!Path', Path_yaml_constructor)
    yaml.add_multi_representer(Path, Path_yaml_representer)
