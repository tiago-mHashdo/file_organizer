# File Organizer Script

The File Organizer script is a Python tool designed to organize files based on their file extensions using a configuration file. It allows you to specify source and destination folders, as well as custom folder mappings for different file extensions. Additionally, it provides options for replacing files with the same name and moving uncategorized files to an "Others" folder.

## Prerequisites

- Python 3.x installed on your system.

## Usage

1. First, ensure that you have a valid configuration file (e.g., `config.json`) containing the necessary settings for file organization. Refer to the section below for details on the configuration file.

2. Run the script with the appropriate command-line arguments:

```bash
python file_organizer.py --config path/to/config.json --replace yes --others yes
```
## Command-line Arguments

    --config or -c: The path to the configuration file. Defaults to config.json if not specified explicitly.
    --replace or -r: Specify whether to replace files in the destination folder if files with the same names already exist. Acceptable values are yes or y for replacement and no or n to avoid replacement. Defaults to yes.
    --others or -o: Specify whether to move uncategorized files to an "Others" folder. Acceptable values are yes or y for moving uncategorized files and no or n to keep them in the source folder. Defaults to yes.

Note: The --backup argument mentioned in the script comments is not implemented. Please ignore it.
Configuration File

The configuration file (config.json by default) is used to define the source folder, destination folder, and mappings of file extensions to specific destination folders. Make sure to create and adjust the configuration file according to your requirements. Below is an example of a valid config.json file:

json

{
  "downloads_folder": "/path/to/source_folder",
  "destination_folder": "/path/to/destination_folder",
  "extensions_mapping": {
    "Images": [".jpg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".avi", ".mkv"]
  }
}

In this example, the script will organize files with extensions .jpg, .png, and .gif into the Images folder, files with extensions .pdf, .docx, and .txt into the Documents folder, and files with extensions .mp4, .avi, and .mkv into the Videos folder. Any other files will be moved to the Others folder if the --others option is set to yes.
Logging

The script logs its progress and any errors to the console. Information about the movement of files, errors encountered, and the total number of files found in the source folder will be displayed during execution.
Important Notes

    Always double-check the configuration file to avoid any accidental data loss. Make sure the source and destination folders are correct before running the script.
    Be cautious when using the --replace option, as it can lead to overwriting files in the destination folder if files with the same names already exist.

Happy organizing!