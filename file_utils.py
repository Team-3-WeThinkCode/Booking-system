import os, json
from os.path import expanduser


def is_non_zero_file(fpath):
    '''
    Checks if json file, with specified filepath, exists and is not empty.

            Parameters:
                    fpath     (str): File filepath

            Returns:
                    True  (boolean): File exists and is not empty
                    False (boolean): File does not exist and/or is empty
    '''

    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def read_data_from_json_file(fpath):
    '''
    Reads data from a json file, specified by filepath, and returns the data.

            Parameters:
                    fpath        (str): File filepath

            Returns:
                    True     (boolean): File exists and is not empty
                    False    (boolean): File does not exist and/or is empty

                    info     (no type): Data read from file path
                    *     (empty dict): If file is empty/does not exist
    '''

    if is_non_zero_file(fpath):
        with open(fpath, 'r') as json_file:
                info = json.load(json_file)
        return True, info
    return False, {}


def write_data_to_json_file(fpath, data):
    '''
    Add specified data to json file, specified by filepath.

            Parameters:
                    fpath (str): File filepath
                    data  (no type): Data to be added to json file
    '''

    with open(fpath, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


def find_home_directory():
    '''
    Returns filepath to user's home directory.

            Returns:
                    home  (str): User's home directory filepath
    '''

    home = expanduser("~")
    return home