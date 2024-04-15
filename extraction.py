from ime.parser.parsers import MetadataExtractor, extract_metadata, flatten_dict_keys_unique_id
from ime.parser.image_parser import ImageProcessor
import pandas as pd
import csv
import json

#inf = '/Volumes/resmed202000005-biru-shared-drive/MyTardisTestData/Haruna_HierarchyStructure/20221113_haruna_RWM_sheep_/20221113_sheep_RWM_cd34_x20_0.12umpiz_01.czi'
#inf = '/Users/xli677/Desktop/MJD_Rock_Sample_03-Spot000001.ims'
#inf = "/Volumes/resmed202000005-biru-shared-drive/MyTardisTestData/Haruna_HierarchyStructure/20221113_haruna_rwm_cd34/20221113_slide3-1_humanRWM_cd34_x5_0.62umpix_01-Image Export-13/20221113_slide3-1_humanRWM_cd34_x5_0.62umpix_01-Image Export-13_c1.tif"
#inf = "/Volumes/resmed202000005-biru-shared-drive/MyTardisTestData/Jacqui/Zeiss\ LSM\ 800\ data/63x_zseries.czi"
#inf = "/Volumes/resmed202000005-biru-shared-drive/MyTardisTestData/Jacqui/Zeiss LSM 800 data/63x_zseries.czi"
#inf = "gfap_map2_63X_Z_ZOOM.czi"
inf = "63x_triple_MolProbesSlideFluocells2_AS.czi"
#inf="63x_zseries.czi"
#inf = "../test.tif"

imagep = ImageProcessor()
xml_string = imagep.get_omexml_metadata(inf)
my_dict = MetadataExtractor.xml_to_dict(xml_string)
        
# clean the raw dictionary to remove the first layer and @ symbol from the keys
my_dict.pop('StructuredAnnotations')
updated_dict = MetadataExtractor.remove_at_symbol(my_dict)

schema = MetadataExtractor.create_schema_czi_oib()
metadata = extract_metadata(updated_dict, schema)

dict = flatten_dict_keys_unique_id(metadata)

#csv_file = 'extracted_metadata_for_ims.csv'
#csv_file = 'extracted_metadata_for_tif.csv'
csv_file = '63x_zseries_shorted.csv'
#csv_file = 'gfap_map2_63X_Z_ZOOM.csv'
# Write the dictionary to CSV
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    for key, value in dict.items():
        writer.writerow([key, value])

"""f = open("tif_metadata.json", "w")
json.dump(my_dict, f, indent=4)"""