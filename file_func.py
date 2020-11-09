import os
from os.path import expanduser
import filecmp


def create_file(filename):
    '''Creates file with given filename'''
    
    file_object  = open(filename,"w+")
    file_object.close()


def add_to_file(filename, text):
    '''Adds given text to file with given filename'''

    file_object = open(filename, "w+")
    file_object.write(text)
    file_object.close()


def read_content_from_file(filename):
    '''
    Retrieves content from file with given filename
    :return: content from file in string format
    '''

    file_object = open(filename, "r")
    content = file_object.read()
    return content


def find_home_directory():
    '''
    :return: home directory path
    '''

    home = expanduser("~")
    return home


def delete_file(filename):
    '''Deletes file with given filename'''

    os.remove(filename)


def hide_file(filename):
    '''
    Converts file into hidden file
    :return: hidden file's filename
    '''

    if not filename[0] == '.':
        new_filename = os.path.join(os.path.dirname(filename),'.' + os.path.basename(filename))
        os.rename(filename, new_filename)
        return new_filename
    return filename


def create_hidden_file_in_user_directory(filename):
    '''
    Creates hidden file in user's home directory
    :return: hidden file's filename
    '''

    home = find_home_directory()
    path = str(home)+'/'+str(filename)
    create_file(path)
    new_filename = hide_file(path)
    return new_filename


def is_file_content_the_same(filename_1, filename_2):
    '''
    Checks if both files have the exact same content
    :return: True if content is identical
    '''

    return filecmp.cmp(filename_1,filename_2,shallow=False)