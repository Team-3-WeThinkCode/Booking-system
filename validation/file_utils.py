import os
from os.path import expanduser

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def add_data_to_json_file_with_dict(fpath, data, key):
    try:
        if is_non_zero_file(fpath):
            with open(fpath, 'r') as json_file:
                    info = json.load(json_file)
            info[key].append(data)
            with open(fpath, 'w') as f:
                    json.dump(info, f, sort_keys=False, indent=4)
        else:
            with open(fpath, 'w') as json_file:
                json.dump(data, json_file, sort_keys=False, indent=4)
        return True
    except:
        return False


def find_home_directory():
    home = expanduser("~")
    return home


if __name__ == "__main__":
    print(find_home_directory())