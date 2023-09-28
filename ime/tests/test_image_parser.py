from ime.parser.parsers import MetadataExtractor, extract_metadata, flatten_dict_keys_unique_id
from ime.parser.image_parser import ImageProcessor
from pathlib import Path
import logging
import bioformats, javabridge, yaml



def test_xml_to_dict():
    logging.basicConfig(level=logging.WARNING)
    javabridge.start_vm(class_path=bioformats.JARS)
    file_name = '20190812 HF 01 stack.oib'
    xml_string = bioformats.get_omexml_metadata(file_name)
    my_dict = MetadataExtractor.xml_to_dict(xml_string)
    schema_czi = MetadataExtractor.create_schema_czi()
            # clean the raw dictionary to remove the first layer and @ symbol from the keys
    updated_dict = MetadataExtractor.remove_at_symbol(my_dict)
    metadata = extract_metadata(updated_dict, schema_czi)
    
    #print(schema_czi)
    print(metadata)

    javabridge.kill_vm() 