import os

class File:

    def __init__(self, path):
        if os.path.isfile(path):
            self.path = path 
        else:
            raise FileExistsError(f"The provided path is not a regula file. Path: {path}")   
        
    def get_extension(self):
        return os.path.splitext(self.path)[1].lower()