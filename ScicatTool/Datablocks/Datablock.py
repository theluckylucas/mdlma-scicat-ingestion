import time

from .APIKeys import *
from ..Datasets.Consts import TYPE_RAW, TYPE_DERIVED, PID_PREFIX
from ..Datasets.APIKeys import TYPE, PID
from ..Filesystem.FSInfo import get_creation_date, get_ownername, file_size


class OrigDatablockBuilder():
    class ValidationError(Exception):
        MESSAGE = "Validation failed for the following properties, either missing or unknown: {}. "+\
                  "Please check scicatproject.github.io/api-documentation/ for valid keys."
        
        def __init__(self, args):
            self.args = args
            
        def __str__(self):
            return self.MESSAGE.format(', '.join(self.args))
    
    def __init__(self, source_folder):
        super().__init__()
        self.datablock = {}
        self.source_folder = source_folder
    
    def args(self, args):
        return self.owner_group(args.ownergroup).\
            access_groups(args.accessgroups)

    def size(self, size : int):
        self.datablock[SIZE] = size
        return self

    def access_groups(self, access_groups : list):
        self.datablock[ACCESS_GROUPS] = access_groups
        return self

    def owner_group(self, owner_group : str):
        self.datablock[OWNER_GROUP] = owner_group
        return self

    def dataset_id(self, dataset_dict : dict):
        dataset_id = PID_PREFIX + dataset_dict[PID]
        if dataset_dict[TYPE] == TYPE_DERIVED:
            self.datablock[DERIVED_DATASET_ID] = dataset_id
        elif dataset_dict[TYPE] == TYPE_RAW:
            self.datablock[RAW_DATASET_ID] = dataset_id
        self.datablock[DATASET_ID] = dataset_id
        return self

    def data_file_list(self, filename_list : list):
        result = []
        for filename_relative in filename_list:
            full_path = "{}/{}".format(self.source_folder, filename_relative)
            datafile = {
                PATH: filename_relative,
                SIZE: file_size(self.source_folder, filename_relative),
                TIME: get_creation_date(full_path),
                UID: get_ownername(full_path)
            }
            result += [datafile]
        self.datablock[DATA_FILE_LIST] = result
        return self

    def _invalid_datafiles(self):
        invalids = set()
        
        # Illegal keys
        for item in self.datablock[DATA_FILE_LIST]:
            for key in item.keys():
                if key not in PROPERTIES_DATAFILE:
                    invalids.add(key)
        
        # Required keys
        for item in self.datablock[DATA_FILE_LIST]:
            for key in REQUIRED_PROPERTIES_DATAFILE:
                if key not in item.keys():
                    invalids.add(key)
                
        return invalids


    def _invalid(self):
        invalids = self._invalid_datafiles()
        
        # Illegal keys
        for key in self.datablock.keys():
            if key not in PROPERTIES_DATABLOCK:
                invalids.add(key)
        
        # Required keys
        for key in REQUIRED_PROPERTIES_DATABLOCK_ORIGINAL:
            if key not in self.datablock.keys():
                invalids.add(key)
                
        return invalids
            
    def build(self):
        invalids = self._invalid()
        if invalids:
            raise self.ValidationError(invalids)
        return self.datablock
