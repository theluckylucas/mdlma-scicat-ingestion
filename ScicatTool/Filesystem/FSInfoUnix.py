from os import stat
from pwd import getpwuid


def get_ownername(filename):
    uid = stat(filename).st_uid
    try:
        return getpwuid(uid).pw_name
    except:
        return str(uid)
