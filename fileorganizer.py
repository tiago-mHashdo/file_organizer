import os
import json
import argparse
import logging


def get_from_config_file(config_file, config_key):
    if config_key in config_file:
        return config_file[config_key]

    else:
        raise KeyError(f"Failed to get the following configuration key: {config_key}. "
                       f"Please ensure that the configuration key exists in your configuration file.")


def validate_path_existance(path):
    if not os.path.exists(path):
        logging.error(f"Invalid path: {path}")
        exit()


def get_config_from_path(config_file_path):
    try:
        with open(config_file_path) as config_file:
            return json.load(config_file)

    except FileNotFoundError as e:
        logging.error(f"Invalid config file: {e}")
        return


def move_files_by_extension(config_file_path, options):
    config = get_config_from_path(config_file_path)

    src_folder = get_from_config_file(config, "downloads_folder")
    dst_folder = get_from_config_file(config, "destination_folder")
    extensions_mapping = get_from_config_file(config, "extensions_mapping")

    validate_path_existance(src_folder)
    validate_path_existance(dst_folder)
    logging.info(f"Moving files from: {src_folder} -> to: {dst_folder}")
    
    folder_entries = os.listdir(src_folder)
    logging.info(
        f"Found {len(folder_entries)} entries in the provided folder: {src_folder}")

    for filename in folder_entries:
        src_path = os.path.join(src_folder, filename)

        if os.path.isfile(src_path):
            was_moved = False
            extension = os.path.splitext(filename)[1]
            for folder, extensions in extensions_mapping.items():
                new_dst_folder = os.path.join(dst_folder, folder)
                os.makedirs(new_dst_folder, exist_ok=True)
                new_dst_path =  os.path.join(new_dst_folder, filename)
                if extension.lower() in extensions:
                    move_file_to_new_directory(
                        src_path, new_dst_path, options["replace"])
                    was_moved = True
                    break

            if options["others"] and not was_moved:
                new_dst_folder = os.path.join(dst_folder, "Others")
                os.makedirs(new_dst_folder, exist_ok=True)
                new_dst_path =  os.path.join(new_dst_folder, filename)

                move_file_to_new_directory(
                    src_path, new_dst_path, options["replace"])


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
    parser = argparse.ArgumentParser(prog="File Organizer",
                                     description="Move files based on extensions using a configuration file.")

    parser.add_argument("--config", "-c", type=str, default="config.json",
                        help="The path to the configurations file. Defaults to \"config.json\"")
    parser.add_argument("--replace", "-r", type=str, default="y", choices=["yes", "y", "no", "n"],
                        help="Replace files in case there are files on the destination folder with the same name. Defaults to \"yes\"")
    parser.add_argument("--backup", "-b", type=str, default="y", choices=["yes", "y", "no", "n"],
                        help="Move uncategorized files to a \"Others\" folder. Defaults to \"yes\"") #TODO
    parser.add_argument("--others", "-o", type=str, default="y", choices=["yes", "y", "no", "n"],
                        help="Move uncategorized files to a \"Others\" folder. Defaults to \"yes\"")

    return parser.parse_args()


def config_logger():
    log_format = '%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s - %(name)s -| %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)


def get_arguments_as_bools(args):
    possible_arg_value = ["yes", "y", "no", "n"]
    args_as_bools = {}

    for arg in vars(args):

        if getattr(args, arg) in possible_arg_value:
            args_as_bools[arg] = True if (
                getattr(args, arg) == "yes" or getattr(args, arg) == 'y') else False

    return args_as_bools


if _name_ == "_main_":
    args = parse_arguments()
    config_logger()
    logging.info(f"Staring script")
    options = get_arguments_as_bools(args)
    logging.info(f"Current options: {options}")

    move_files_by_extension(args.config, options)