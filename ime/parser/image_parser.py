import jpype
import jpype.imports
from jpype.types import *
from ime.parser.parsers import MetadataExtractor, extract_metadata, flatten_dict_keys_unique_id
from pathlib import Path

loci = jpype.JPackage("loci")
if not jpype.isJVMStarted(): # type: ignore
    jpype.startJVM(classpath="ime/tests/testdata/bioformats_package.jar", convertStrings=True) # type: ignore

from loci import *
from loci.formats import ImageReader
from loci.common.services import ServiceFactory
from loci.formats.services import OMEXMLService
from loci.formats.in_ import DefaultMetadataOptions
from loci.formats.in_ import MetadataLevel
loci.common.DebugTools.setRootLevel("ERROR")

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
    def get_metadata(self, inf: str):
        """
        Retrieves metadata from an image file.

        Args:
            inf (str): The path to the image file.

        Returns:
            dict[str,str]: The extracted metadata if the file is a CZI or OIB file.
            Otherwise, returns a nempty dictionary.

        """
        suffix = Path(inf).suffix
        suffix_available = ['.czi', '.oib']
        if suffix not in suffix_available:
            return dict()
        else:
            # get xml string
            xml_string = self.get_omexml_metadata(inf)
            # convert xml string to dictionary
            my_dict = MetadataExtractor.xml_to_dict(xml_string)
            # create schema
            schema_czi = MetadataExtractor.create_schema_czi() # type: ignore
            # clean the raw dictionary to remove the first layer and @ symbol from the keys
            updated_dict = MetadataExtractor.remove_at_symbol(my_dict)
            # extract metadata that matchs schema
            metadata = extract_metadata(updated_dict, schema_czi)
            return flatten_dict_keys_unique_id(metadata)
          
    def get_omexml_metadata(self, inf: str):
        '''Read the OME metadata from a file using Bio-formats

        :param path: path to the file

        :param groupfiles: utilize the groupfiles option to take the directory structure
                 into account.

        :returns: the metdata as XML.

        '''
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