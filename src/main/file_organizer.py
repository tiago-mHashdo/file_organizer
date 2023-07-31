import os
import json
import argparse
import logging
from domain.configuration import Configuration
from domain.configuration_file import ConfigurationFile
from domain.file import File


def move_files_by_extension(options):
    file = ConfigurationFile(args.config)
    configuration = Configuration(file, options)

    logging.info(
        f"Moving files from: {configuration.source_folder} -> to: {configuration.destination_folder}"
    )

    folder_entries = os.listdir(configuration.source_folder)
    logging.info(
        f"Found {len(folder_entries)} entries in the provided folder: {configuration.source_folder}"
    )

    for filename in folder_entries:
        file = File(os.path.join(configuration.source_folder, filename))
        was_moved = False
        for folder, extensions in configuration.get_mappings_items():
            new_dst_folder = os.path.join(configuration.destination_folder, folder)
            os.makedirs(new_dst_folder, exist_ok=True)
            new_file_path = os.path.join(new_dst_folder, filename)
            if file.get_extension in extensions:
                move_file_to_new_directory(
                    file.path,
                    new_file_path,
                    configuration.get_option_as_bool("replace"),
                )
                logging.info(f"Moving file from: {file.path} -> to: {new_file_path}")
                was_moved = True
                break
            if configuration.get_option_as_bool("others") and not was_moved:
                new_dst_folder = os.path.join(
                    configuration.destination_folder, "Others"
                )
                os.makedirs(new_dst_folder, exist_ok=True)
                new_file_path = os.path.join(new_dst_folder, filename)
                move_file_to_new_directory(
                    file.path,
                    new_file_path,
                    configuration.get_option_as_bool("replace"),
                )


def move_file_to_new_directory(src_path, dst_path, replace):
    try:
        if replace:
            os.replace(src_path, dst_path)
        else:
            os.rename(src_path, dst_path)

        logging.info(f"Moved: {src_path} -> {dst_path}")

    except Exception as e:
        logging.error(f"Error moving {src_path}: {e}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="File Organizer",
        description="Move files based on extensions using a configuration file.",
    )

    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="config.json",
        help='The path to the configurations file. Defaults to "config.json"',
    )
    parser.add_argument(
        "--replace",
        "-r",
        type=str,
        default="y",
        choices=["yes", "y", "no", "n"],
        help='Replace files in case there are files on the destination folder with the same name. Defaults to "yes"',
    )
    parser.add_argument(
        "--backup",
        "-b",
        type=str,
        default="y",
        choices=["yes", "y", "no", "n"],
        help='Move uncategorized files to a "Others" folder. Defaults to "yes"',
    )  # TODO
    parser.add_argument(
        "--others",
        "-o",
        type=str,
        default="y",
        choices=["yes", "y", "no", "n"],
        help='Move uncategorized files to a "Others" folder. Defaults to "yes"',
    )

    return parser.parse_args()


def config_logger():
    log_format = "%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s - %(name)s -| %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)


if __name__ == "__main__":
    args = parse_arguments()
    config_logger()
    logging.info(f"Staring script")
    logging.info(f"Current args: {args}")

    move_files_by_extension(args)
