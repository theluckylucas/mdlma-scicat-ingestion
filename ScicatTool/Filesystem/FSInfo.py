import getpass
import platform
from os import stat, listdir, path, scandir, walk
from datetime import datetime

FOLLOW_SYMLINKS = False
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_ext(filename):
    pos = filename.rfind('.')
    ext = filename[pos+1:]
    return ext


def get_username():
    return getpass.getuser()


def path_exists(directory):
    return path.exists(directory)


def file_size(directory, filename_relative):
    full_path = path.join(directory, filename_relative)
    if not FOLLOW_SYMLINKS and path.islink(full_path):
        return 0
    return path.getsize(full_path)


def folder_total_size(directory):
    return sum(file_size(dirpath,filename) for dirpath, dirnames, filenames in walk(directory, followlinks=FOLLOW_SYMLINKS) for filename in filenames)


def list_files(directory, exts=[]):
    return [f.name for f in scandir(directory) if f.is_file(follow_symlinks=FOLLOW_SYMLINKS) and path.splitext(f.name)[1] in exts]


def list_dirs(directory):
    return [f.name for f in scandir(directory) if f.is_dir(follow_symlinks=FOLLOW_SYMLINKS)]


def get_creation_date(filename):
    if platform.system() == 'Windows':
        return datetime.fromtimestamp(path.getctime(filename)).strftime(DATETIME_FORMAT)
    else:
        file_stat = stat(filename)
        try:
            return file_stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return datetime.fromtimestamp(file_stat.st_mtime).strftime(DATETIME_FORMAT)