import json
import os
from file import File

class InvalidFileError(Exception):
    pass


class ConfigurationFile(File):
    def __init__(self, path):
        super(ConfigurationFile, self).__init__(path)

        try:
            with open(path) as file:
                self.content = json.load(file)
                if not isinstance(self.content, (dict, list)):
                    raise InvalidFileError(
                        "JSON content should be a dictionary or list"
                    )
        except json.JSONDecodeError as e:
            raise InvalidFileError(f"Invalid JSON format in file: {e}")
        except Exception as e:
            raise InvalidFileError(f"Error while reading file: {e}")


    
    def get_from_file(self, key):
            if key in self.content:
                return self.content[key] 
            else: 
                raise KeyError(f"Could not find the requested key this file. File: {self.path}\n Key: {key}")      


    
    def get_from_file_with_type(self, key, type):
        if type == None:
            self.get_from_file(self, key)
        else:
            if key in self.content and isinstance(self.content[key], type):
                self.get_from_file(self, key)
            else:
                raise TypeError(f"Could not find the requested key with the requested type. Key: {key}\n Type: {type}")    
