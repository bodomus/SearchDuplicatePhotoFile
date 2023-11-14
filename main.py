import os
import glob

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
    directory_to_search = 'j:/Photo/2021/2021-08-08/'
    directory_to_enumerate = 'z:/Photo1/DCIM/100CANON/'
    files_for_search = enumerate_files(directory_to_enumerate)
    for f in files_for_search:
        filename, file_extension = os.path.splitext(f)
        found_files = find_files_by_name_and_extension(directory_to_search, filename, file_extension)
        if len(found_files) > 0:
            for foundf in found_files:
                print(f"Find file {foundf} search: {found_files} found.")
        else:
            print(f"File \"{f}\" not found in {directory_to_search} and subdirectories.")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
