import getpass
from os import stat, listdir
from pwd import getpwuid


def current_username():
    return getpass.getuser()


def file_ownername(filename):
    return getpwuid(stat(filename).st_uid).pw_name


def first_file(directory):
    return listdir(directory)[0]