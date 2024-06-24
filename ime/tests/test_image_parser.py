from ime.parser.parsers import MetadataExtractor, extract_metadata, flatten_dict_keys_unique_id
from ime.parser.image_parser import ImageProcessor

def test_get_metadata():
    from ime.parser.image_parser import ImageProcessor
    file_name = 'ime/tests/testdata/good image 02.oib'
    image_processor = ImageProcessor()
    metadata = image_processor.get_metadata(file_name)
    assert metadata['Instrument|Detector|Detector:0:0|ID'] == 'Detector:0:0'
    assert metadata['Instrument|Objective|LensNA'] == '1.35'