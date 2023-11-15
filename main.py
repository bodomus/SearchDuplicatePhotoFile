import os
from colorama import Fore, Style
import exifread
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def get_file_size(file_path):
    """
    Get the size of a file in bytes.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        int: The size of the file in bytes.
    """
    return os.path.getsize(file_path)


def read_exif_date(file):
    with open(file, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        date_taken = tags["EXIF DateTimeOriginal"]
        return date_taken


def get_creation_date(file_path):
    try:
        # Open the image file
        img = Image.open(file_path)

        # Extract Exif data
        exif_data = img._getexif()

        # Iterate over Exif data and look for the creation date
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'DateTimeOriginal':
                return value

    except (AttributeError, KeyError, IndexError):
        # Handle cases where the image has no Exif data or no creation date information
        pass

    return None


def enumerate_files(directory):
    files_list = os.listdir(directory)
    return files_list


def find_files_by_name_and_extension(directory, file_name, file_extension):
    # Initialize an empty list to store matching file paths
    matching_files = []
    # Use os.walk to traverse the directory tree
    for root, dirs, files in os.walk(directory):
        # Process the files in the current directory
        for current_file in files:
            if current_file == f"{file_name}{file_extension}":
                file_path = os.path.join(root, current_file)
                matching_files.append(file_path)

    return matching_files


def make_decision(source_file_path, destination_file_path):
    """
    Make decision. Is source file the same as destination

    Parameters:
        source_file_path (str): The path to the file.

    Returns:
        bool: true if files are identity.
    """

    dt = read_exif_date(source_file_path)
    dtd = read_exif_date(destination_file_path)

    source_file_size = get_file_size(source_file_path)
    destination_file_size = get_file_size(destination_file_path)

    return (str(dt) == str(dtd)) and (source_file_size == destination_file_size)


target_file_name = 'example'
target_file_extension = 'txt'

if __name__ == '__main__':
    # Example usage:
    directory_to_search = 'j:/Photo/'
    directory_to_original_file_enumerate = 'z:/Photo1/DCIM/100CANON/'
    print(Fore.RED + "File " + Style.RESET_ALL)
    files_for_search = enumerate_files(directory_to_original_file_enumerate)
    for f in files_for_search:
        filename, file_extension = os.path.splitext(f)
        found_files = find_files_by_name_and_extension(directory_to_search, filename, file_extension)
        if len(found_files) > 0:
            for foundf in found_files:
                dt = read_exif_date(directory_to_original_file_enumerate + filename + file_extension)
                dtd = read_exif_date(foundf)
                if str(dt) == str(dtd):
                    print("For file ")
                    print(Fore.GREEN + f"{f}" + Style.RESET_ALL)
                    print(
                        "was found files:" + Fore.GREEN + f"{foundf}" + Style.RESET_ALL + f"DateTime file: {read_exif_date(foundf)} Count files: {len(found_files)}")
        else:
            print(
                "File " + Fore.RED + f" \"{f}\" " + Style.RESET_ALL + " not found in {directory_to_search} and subdirectories.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
