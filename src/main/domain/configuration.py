import json
from main.domain.configuration_file import ConfigurationFile


class Configuration:
    options_values = ["yes", "y", "no", "n"]

    def __init__(self, content: ConfigurationFile, options):
        self.content = content
        self.source_folder = content.get_from_file_with_type("source_folder", str)
        self.destination_folder = content.get_from_file_with_type(
            "destination_folder", str
        )
        self.mappings = content.get_from_file_with_type("extensions_mappings", dict)
        self.options = options

    def get_option_as_bool(self, option):
        option_as_bool = False
        if getattr(self.options, option) in self.options_values:
            return (
                True
                if (
                    getattr(self.options, option) == "yes"
                    or getattr(self.options, option) == "y"
                )
                else False
            )

        return option_as_bool
    
    def get_mappings_items(self):
        return self.mappings.items()