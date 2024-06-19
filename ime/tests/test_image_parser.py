import pytest

from ime.parser.image_parser import ImageProcessor


# @pytest.mark.skip(reason="Seg faulting?")
def test_get_metadata():
    file_name = "ime/tests/testdata/good image 02.oib"
    image_processor = ImageProcessor()
    # metadata = image_processor.get_metadata(file_name)
    assert metadata["Instrument|Detector|Detector:0:0|Gain"] == "1000.0"
    assert metadata["Instrument|Detector|Detector:0:0|Type"] == "PMT"
