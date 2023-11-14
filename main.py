import os
import glob
from PIL import Image
from PIL.ExifTags import TAGS
import exifread
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def read_exif_date(file):
    with open(file, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        dateTaken = tags["EXIF DateTimeOriginal"]
        return dateTaken


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
    current_file = file_name + file_extension
    # Use os.walk to traverse the directory tree
    for root, dirs, files in os.walk(directory):
        # Process the files in the current directory
        for current_file in files:
            if current_file == f"{file_name}{file_extension}":
                file_path = os.path.join(root, current_file)
                matching_files.append(file_path)

    return matching_files


target_file_name = 'example'
target_file_extension = 'txt'

if __name__ == '__main__':
    # Example usage:
    directory_to_search = 'j:/Photo/'
    directory_to_original_file_enumerate = 'z:/Photo1/DCIM/100CANON/'
    files_for_search = enumerate_files(directory_to_original_file_enumerate)
    for f in files_for_search:
        filename, file_extension = os.path.splitext(f)
        found_files = find_files_by_name_and_extension(directory_to_search, filename, file_extension)
        if len(found_files) > 0:
            for foundf in found_files:
                dt = read_exif_date(directory_to_original_file_enumerate + filename+file_extension)
                dtd = read_exif_date(foundf)
                if str(dt) == str(dtd):
                    print(
                        f"Find file {bcolors.BOLD}{foundf}{bcolors.ENDC} search: {found_files} found. DateTime file: {bcolors.BOLD}{read_exif_date(foundf)}{bcolors.ENDC} Count files: {len(found_files)}")
        else:
            print(f"File {bcolors.BOLD}\"{f}\"{bcolors.ENDC} not found in {directory_to_search} and subdirectories.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
