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

def test_datafile_metadata_saved_as_none_if_empty(tmp_path: Path) -> None:
    """Tests whether for datafile, if there is no metadata, it is saved as a None, rather 
    than an empty dict. This is expected by the ingestion script.

    Args:
        metadata (IngestionMetadata): The ingestion metadata.
    """
    # Create a datafile in the same tmp path.
    tmp_datafile = tmp_path / "data.txt"
    tmp_datafile.touch()
    # Create a new metadata collection, with the datafile.
    metadata = IngestionMetadata()
    df = Datafile()
    df.path_abs = tmp_datafile
    df.metadata = {}
    metadata.datafiles.append(df)
    new_path = str(tmp_path / "new.yaml")
    # Save the ingestion file.
    metadata.to_file(new_path)
    # Load the newly saved ingestion file and find the datafile again.
    new_metadata = IngestionMetadata.from_file(new_path)
    assert len(new_metadata.datafiles) == 1
    # Check that the metadata is now None.
    assert new_metadata.datafiles[0].metadata is None