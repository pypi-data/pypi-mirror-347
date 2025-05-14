import fileinput
import hashlib
import os
import re
import shutil
from typing import Dict, List


def get_list_of_files_in_cur_folder(dir_path: str, pattern: str) -> List[str]:
    """
    For the given path, get the list of all files in the current folder

    Parameters
    -----------
    dir_path : str
        The directory path to look into
    pattern : str
        The pattern of the files to look for

    Returns
    -----------
    The list of file complete paths
    """
    cur_file_list = os.listdir(dir_path)
    file_list = list()
    # Iterate over all the entries
    for entry in cur_file_list:
        # Create full path
        full_path = os.path.join(dir_path, entry)
        if not os.path.isdir(full_path):
            if pattern is not None:
                # Checks if the pattern is matching the file
                if re.search(re.compile(pattern), entry) is not None:
                    file_list.append(full_path)
            else:
                file_list.append(full_path)
    return file_list


def get_list_of_files(dir_path: str) -> List[str]:
    """
    For the given path, get the List of all files in the directory tree recursively

    Parameters
    -----------
    dir_path : str
        The directory path to look into

    Returns
    -----------
    The list of file complete paths

    """
    # create a list of file and sub directories
    # names in the given directory
    cur_file_list = os.listdir(dir_path)
    file_list: List[str] = []
    # Iterate over all the entries
    for entry in cur_file_list:
        # Create full path
        full_path = os.path.join(dir_path, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            file_list = file_list + get_list_of_files(full_path)
        else:
            file_list.append(full_path)
    return file_list


"""
    For the given path, get the List of all files in the directory tree 
    Recursive function
"""


def get_list_of_files_in_relative_path(
    dir_name: str, relative_path: str = "."
) -> List[str]:
    # create a list of file and sub directories
    # names in the given directory
    list_of_files = os.listdir(dir_name)
    all_files: List[str] = []
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        current_relative_path = os.path.join(relative_path, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files_in_relative_path(
                full_path, current_relative_path
            )
        else:
            all_files.append(current_relative_path)

    return all_files


"""
    For the given path, get the List of all files in the directory tree 
    Recursive function
"""


def get_list_of_directories_in_relative_path(
    dir_name: str, relative_path: str = "."
) -> List[str]:
    # create a list of file and sub directories
    # names in the given directory
    list_of_files = os.listdir(dir_name)
    all_directories = list()
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        current_relative_path = os.path.join(relative_path, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_directories.append(current_relative_path)
            all_directories = (
                all_directories
                + get_list_of_directories_in_relative_path(
                    full_path, current_relative_path
                )
            )
    return all_directories


def get_list_of_directories(dir_name: str) -> List[str]:
    """
    For the given path, get the List of all files in the directory tree
    Recursive function

    Parameters
    -----------
    dir_name : str
        The directory absolute path to look into

    Returns
    -----------
    directory_list : list
        A list containing all the folders found in the directory provided
    """
    # create a list of file and sub directories
    # names in the given directory
    list_of_files = os.listdir(dir_name)
    directory_list = list()
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            directory_list.append(full_path)
            directory_list = directory_list + get_list_of_directories(full_path)
    return directory_list


"""
    Removes all the files in the provided directory
"""


def remove_all_files_in_directory(dir_name: str) -> None:
    list_of_files = get_list_of_files_in_relative_path(dir_name)
    for file_relative_path in list_of_files:
        os.remove(os.path.join(dir_name, file_relative_path))


def get_file_base_name_wo_extension(file_path: str) -> str:
    """
    Get the base name of a file

    Parameters
    -----------
    file_path : str
        The file complete path

    Returns
    -----------
    baseName : str
        The base name of the file without the extension
    """
    split_file_name = os.path.basename(file_path).split(".")
    split_file_name.pop(len(split_file_name) - 1)
    return ".".join(split_file_name)


def unpack_archive(
    archive_file_path: str,
    extraction_folder: str,
    remove_archive_after_unpack: bool = False,
    extraction_inside_current_folder: bool = False,
) -> str:
    """
    Unpacks an archive in a folder with the same base name as the archive located in
    the extraction folder provided

    Parameters
    -----------
    archive_file_path : str
        The archive complete path

    extraction_folder : str
        The folder to extraction the archive into

    remove_archive_after_unpack : bool
        A flag to force the deletion of the archive after the unpack

    extraction_inside_current_folder: bool
        A flag to extract inside the current folder, instead of in a dedicated folder

    Returns
    -----------
    archive_extraction_folder : str
        The complete path of the extracted archive
    """
    if extraction_inside_current_folder:
        archive_extraction_folder = os.path.dirname(archive_file_path)
    else:
        archive_file_base_name = get_file_base_name_wo_extension(
            archive_file_path
        )
        archive_extraction_folder = os.path.join(
            extraction_folder, archive_file_base_name
        )
        os.makedirs(archive_extraction_folder, exist_ok=False)
    shutil.unpack_archive(archive_file_path, archive_extraction_folder)
    if remove_archive_after_unpack:
        os.remove(archive_file_path)
    return archive_extraction_folder


def make_archive_from_folder(
    archive_generation_folder_path: str,
    folder_to_archive: str,
    remove_folder_after_pack: bool = False,
) -> str:
    """
    Makes an archive from the folder provided into the generation folder path provided

    Parameters
    -----------
    archive_generation_folder_path : str
        The folder path to generate the archive into

    folder_to_archive : str
        The folder to archive

    remove_folder_after_pack : bool
        A flag to force the deletion of the packed folder after archive is created

    Returns
    -----------
    generated_archive_path : str
        The complete path of the generated archive

    """
    folder_to_archive_complete_path = os.path.join(
        archive_generation_folder_path, folder_to_archive
    )
    generated_archive_path = shutil.make_archive(
        archive_generation_folder_path, "zip", folder_to_archive_complete_path
    )
    if remove_folder_after_pack:
        shutil.rmtree(folder_to_archive_complete_path)
    return generated_archive_path


def hash(file_path: str) -> str:
    """
    Returns the standard hash of a file

    Parameters
    -----------
    file_path : str
        The file path

    Returns
    -----------
    fileHash : _Hash
        The file hash

    """
    with open(file_path, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    return h.upper()


def replace_text_in_file(
    file_path: str, original_str: str, new_str: str
) -> None:
    """
    Replace a text inside an existing file

    Parameters
    -----------
    file_path : str
        The file path

    original_str : str
        The original string

    new_str : str
        The new string

    Returns
    -----------
    None

    """
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            print(line.replace(original_str, new_str))


def replace_strings_in_file(
    file_path: str, replacement_dict: dict[str, str]
) -> None:
    """
    Replace one to multiple string inside an existing file

    Parameters
    -----------
    filePath : str
        The file path

    replacement_dict : str
        The replacement dictionary linking an original string to the new string that it should be replaced with

    Returns
    -----------
    None

    """
    # Read in the file
    with open(file_path, "r") as file:
        filedata = file.read()

    # Replace the target string
    for original_value, new_value in replacement_dict.items():
        filedata = filedata.replace(original_value, new_value)

    # Write the file out again
    with open(file_path, "w") as file:
        file.write(filedata)


def is_text_in_file(file_path: str, str_to_find: str) -> bool:
    with open(file_path, "r") as file_reader:
        if str_to_find in file_reader.read():
            return True
    return False


def merge_files(merge_file_path: str, files_to_merge: list[str]) -> None:
    with open(merge_file_path, "w") as outfile:
        for file in files_to_merge:
            with open(file) as infile:
                outfile.write(infile.read())


def create_empty_file(file_path: str) -> None:
    open(file_path, "a").close()


def load_file_into_dict(file_path: str) -> Dict[str, str]:
    """
    Loads the content of a file into a dictionary where the key is the file name
    (without the extension) and the value is the complete content of the file.

    Parameters
    -----------
    file_path : str
        The path to the file.

    Returns
    -----------
    Dict[str, str]
        A dictionary with the file name (without extension) as key and the file content as value.

    """
    key, _ext = os.path.splitext(os.path.basename(file_path))

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {key: content}
