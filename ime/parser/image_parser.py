"""image_parser.py - Metadata extractor using bioformats."""
import logging
from pathlib import Path

import jpype
import jpype.imports
from jpype.types import *

from ime.parser.parsers import (
    SCHEMA_CARL_ZEISS,
    MetadataExtractor,
    extract_metadata,
    flatten_dict_keys_unique_id,
)
from ime.utils import path_for_asset

logger = logging.getLogger(__name__)

try:
    # Try to start the JVM and import Java Bioformats classes
    bioformats_jar_path = path_for_asset(Path("resources/bioformats_package.jar"))
    if not jpype.isJVMStarted():  # type: ignore
        jpype.startJVM(classpath=[str(bioformats_jar_path)], convertStrings=True)  # type: ignore
    import loci.common
    from loci.common.services import ServiceFactory
    from loci.formats import ImageReader
    from loci.formats.in_ import DefaultMetadataOptions, MetadataLevel
    from loci.formats.services import OMEXMLService

    # Set output to be less verbose.
    loci.common.DebugTools.setRootLevel("ERROR")
except ImportError:
    logger.error("Unable to import Bioformats classes.")


class ImageProcessor:
    """
    A class for processing image metadata using bioformats and javabridge.

    Attributes:
        None

    Methods:
        initialize_java_vm: Initializes the Java virtual machine required for bioformats.
        kill_vm: Terminates the Java virtual machine.
        get_metadata: Retrieves metadata from an image file.

    """

    def get_metadata(self, inf: str):
        """
        Retrieves metadata from an image file.

        Args:
            inf (str): The path to the image file.

        Returns:
            dict[str,str]: The extracted metadata if the file is a CZI or OIB file.
            Otherwise, returns a nempty dictionary.

        """
        # Define the suffixes for supported file types
        supported_suffix = [".czi", ".oib", ".tif"]

        # Get the suffix of the file
        suffix = Path(inf).suffix

        # check if the file is a supported file type
        if suffix not in supported_suffix:
            logger.error("Unsupported file type: %s", suffix)
            return {}  # Return an empty dictionary for unsupported file types

        # get xml string and convert it to a dictoionary
        xml_string = self.get_omexml_metadata(inf)
        my_dict = MetadataExtractor.xml_to_dict(xml_string)

        # remove unnecessary item with the key "StructuredAnnotations"
        my_dict.pop("StructuredAnnotations")

        # clean the raw dictionary to remove the first layer and @ symbol from the keys
        updated_dict = MetadataExtractor.remove_at_symbol(my_dict)

        # extract metadata that matchs schema
        metadata = extract_metadata(updated_dict, SCHEMA_CARL_ZEISS)

        return flatten_dict_keys_unique_id(metadata)

    def get_omexml_metadata(self, inf: str):
        """Read the OME metadata from a file using Bio-formats

        :param path: path to the file

        :param groupfiles: utilize the groupfiles option to take the directory structure
                 into account.

        :returns: the metdata as XML.

        """
        reader = ImageReader()
        reader.setGroupFiles(False)
        reader.setOriginalMetadataPopulated(True)
        service = ServiceFactory().getInstance(OMEXMLService)
        metadata = service.createOMEXMLMetadata()

        reader.setMetadataStore(metadata)
        default_metadata_options = DefaultMetadataOptions(MetadataLevel.ALL)
        reader.setMetadataOptions(default_metadata_options)
        reader.setId(inf)
        xml = service.getOMEXML(metadata)
        return xml
