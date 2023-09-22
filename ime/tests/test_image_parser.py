from ime.parser.parsers import MetadataExtractor, extract_metadata, flatten_dict_keys_unique_id
from ime.parser.image_parser import ImageProcessor
from pathlib import Path
import logging

import imagej
import jpype
import scyjava
import jpype.imports

def test_get_metadata():
    from ime.parser.image_parser import ImageProcessor
    file_name = 'ime/tests/testdata/good image 02.oib'
    image_processor = ImageProcessor()
    xml_string = image_processor.get_omexml_metadata(file_name)
    metadata = image_processor.get_metadata(file_name)
    assert metadata['Instrument|Detector|Detector:0:0|Gain'] == '1000.0'
    assert metadata['Instrument|Detector|Detector:0:0|Type'] == 'PMT'