import yaml
from jsonschema import validate, exceptions
import xmltodict
import javabridge
import bioformats

class MetadataExtractor:
    def create_schema_czi():
        """Create a schema for CZI metadata.

        Returns:
            dict: The schema for CZI metadata.
        """
        schema = {
            'Instrument': {
                'Detector': None,
                'Objective': {
                    'ID': 'string',
                    'Model': None,
                    'Immersion': None,
                    'NominalMagnification': None,
                    'WorkingDistance': None,
                    'WorkingDistanceUnit': None
                },
            },
            'Experimenter': {
                'UserName': 'string', 
            },
            'Image':{
                'AcquisitionDate': 'string',
                'Pixels': {
                    'DimensionOrder': 'string',
                    'SizeX': 'integer',
                    'SizeY': 'integer',
                    'Channel': None
                }
            }
        }         
        return schema
    
    def create_schema_test():
        """Create a test schema.

        Returns:
            dict: The test schema.
        """
        schema = {
            'Experimentor': {
                'Username': 'string', 
            },
            'Image':{
                'AcquisitionDate': None,
                'Pixels': {
                    'DimensionOrder': None,
                    'SizeX': None,
                    'SizeY': None,
                }
            }
        }         
        return schema

        
    def xml_to_dict(xml_string: str):
        """Convert XML string to a dictionary.

        Args:
            xml_string (str): The XML string to convert.

        Returns:
            dict: The converted dictionary.
        """
        # convert xml to a dictionary
        data_dict = xmltodict.parse(xml_string)

        # Exclude the first layer of keys
        result_dict = list(data_dict.values())[0]

        return result_dict
    
    def remove_at_symbol(raw_dict: dict):
        """Remove '@' symbol from dictionary keys recursively.

        Args:
            raw_dict (dict): The dictionary to process.
        """
        def remove_at_recursive(obj):
            if isinstance(obj, dict):
                return {key.replace('@', ''): remove_at_recursive(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [remove_at_recursive(element) for element in obj]
            else:
                return obj
            
        return remove_at_recursive(raw_dict)

def extract_metadata(dictionary: dict, schema: dict):
    """Extract metadata from the dictionary based on the schema.

    Args:
        dictionary (dict): The dictionary containing the metadata.
        schema (dict): The schema to match the metadata.

    Returns:
        dict: The extracted metadata.
    """
    extracted_metadata = {}
    for key, value in schema.items():
        if key in dictionary:
            if isinstance(value, dict) and isinstance(dictionary[key], dict):
                extracted_metadata[key] = extract_metadata(dictionary[key], value)
            else:
                extracted_metadata[key] = dictionary[key]
    #extracted_metadata_yaml = yaml.dump(extracted_metadata)
    #extracted_metadata_flattened = flatten_dict_keys(extract_metadata, separator='|')
    return extracted_metadata

def flatten_dict_keys_unique_id(dictionary, separator='|', prefix='', id_key='ID'):
    """
    Flatten the keys of a nested dictionary while incorporating the 'ID' value as part of the key.

    Args:
        dictionary (dict): The dictionary to be flattened.
        separator (str, optional): The separator character used to join the keys. Defaults to '|'.
        prefix (str, optional): The prefix string for nested keys. Defaults to an empty string.
        id_key (str, optional): The key name used to extract unique IDs. Defaults to 'ID'.

    Returns:
        dict: A flattened dictionary with modified keys.

    """
    flattened_dict = {}
    for key, value in dictionary.items():
        new_key = prefix + key if prefix else key
        if isinstance(value, dict):
            flattened_dict.update(flatten_dict_keys_unique_id(value, separator, new_key + separator, id_key=id_key))
        elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
            for item in value:
                if id_key in item:
                    item_key = new_key + separator + str(item[id_key])
                    flattened_dict.update(flatten_dict_keys_unique_id(item, separator, item_key + separator, id_key=id_key))
        else:
            flattened_dict[new_key] = value
    return flattened_dict