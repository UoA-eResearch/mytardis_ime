import bioformats, javabridge, yaml
from ime.parser.parsers import MetadataExtractor, extract_metadata, flatten_dict_keys_unique_id
from pathlib import Path
import logging

class ImageProcessor():
    """
    A class for processing image metadata using bioformats and javabridge.

    Attributes:
        None

    Methods:
        initialize_java_vm: Initializes the Java virtual machine required for bioformats.
        kill_vm: Terminates the Java virtual machine.
        get_metadata: Retrieves metadata from an image file.

    """

    @staticmethod
    def initialize_java_vm():
        """
        Initializes the Java virtual machine required for bioformats.

        Args:
            None

        Returns:
            None

        """
        logging.basicConfig(level=logging.WARNING)
        javabridge.start_vm(class_path=bioformats.JARS)

    @staticmethod
    def kill_vm():
        """
        Terminates the Java virtual machine.

        Args:
            None

        Returns:
            None

        """
        javabridge.kill_vm() 

    def get_metadata(self, inf: str) -> str:
        """
        Retrieves metadata from an image file.

        Args:
            inf (str): The path to the image file.

        Returns:
            str: The extracted metadata if the file is a CZI or OIB file. Otherwise, a string indicating it is not a CZI or OIB file.

        """
        xml_string = bioformats.get_omexml_metadata(inf)
        my_dict = MetadataExtractor.xml_to_dict(xml_string)

        if Path(inf).suffix == '.czi' or Path(inf).suffix == '.oib':
            # create schema
            schema_czi = MetadataExtractor.create_schema_czi()
            # clean the raw dictionary to remove the first layer and @ symbol from the keys
            updated_dict = MetadataExtractor.remove_at_symbol(my_dict)
            # extract metadata that matchs schema
            metadata = extract_metadata(updated_dict, schema_czi)
            metadata_flattened = flatten_dict_keys_unique_id(metadata)
            return metadata_flattened
        else:
            return "Not a CZI file or OIB file."