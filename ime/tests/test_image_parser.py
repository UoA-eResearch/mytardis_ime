from pathlib import Path

import jpype
import jpype.imports
import pytest
import scyjava

from ime.parser.image_parser import ImageProcessor
from ime.parser.parsers import (
    MetadataExtractor,
    extract_metadata,
    flatten_dict_keys_unique_id,
)


@pytest.mark.skip(reason="Seg faulting?")
def test_get_metadata():
    from ime.parser.image_parser import ImageProcessor

    file_name = "ime/tests/testdata/good image 02.oib"
    image_processor = ImageProcessor()
    xml_string = image_processor.get_omexml_metadata(file_name)
    metadata = image_processor.get_metadata(file_name)
    assert metadata["Instrument|Detector|Detector:0:0|Gain"] == "1000.0"
    assert metadata["Instrument|Detector|Detector:0:0|Type"] == "PMT"
