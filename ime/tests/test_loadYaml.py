from ime.models import DifferentDeviceException, IngestionMetadata, Project, Experiment, Dataset, Datafile, DataStatus
import typing
from ime.qt_models import IngestionMetadataModel
from pathlib import Path
import yaml
import logging

def test_loadYaml():
    fileName = "ime/tests/ingestion.yaml"
    metadata = IngestionMetadata()
    metadata.file_path = Path(fileName)
    with open(fileName) as f:
        data_load = f.read()
        objects = yaml.safe_load_all(data_load)
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
    assert len(metadata.projects) == 2
