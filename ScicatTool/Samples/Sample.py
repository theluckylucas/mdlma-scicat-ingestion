import time

from .APIKeys import *
from ..Datasets.Consts import PID_PREFIX, TYPE_DERIVED, TYPE_RAW
from ..Datasets.APIKeys import PID, TYPE


class SampleBuilder():
    class ValidationError(Exception):
        MESSAGE = "Validation failed for the following properties, either missing or unknown: {}. "+\
                  "Please check scicatproject.github.io/api-documentation/ for valid keys."
        
        def __init__(self, args):
            self.args = args
            
        def __str__(self):
            return self.MESSAGE.format(', '.join(self.args))
    
    def __init__(self, sample_id):
        super().__init__()
        self.sample = {SAMPLE_ID: sample_id}
    
    def args(self, args):
        return self.owner_group(args.ownergroup)

    def access_groups(self, access_groups : list):
        self.sample[ACCESS_GROUPS] = access_groups
        return self

    def owner_group(self, owner_group : str):
        self.sample[OWNER_GROUP] = owner_group
        return self

    def description(self, desc : int):
        self.sample[DESCRIPTION] = desc
        return self

    def characteristics(self, characteristics : dict):
        self.sample[SAMPLE_CHARACTERISTICS] = characteristics
        return self

    def dataset_id(self, dataset_dict : dict):
        dataset_id = PID_PREFIX + dataset_dict[PID]
        if dataset_dict[TYPE] == TYPE_DERIVED:
            self.sample[DERIVED_DATASET_ID] = dataset_id
        elif dataset_dict[TYPE] == TYPE_RAW:
            self.sample[RAW_DATASET_ID] = dataset_id
        self.sample[DATASET_ID] = dataset_id
        self.sample[DATASET_IDS] = dataset_id
        return self

    def _invalid(self):
        invalids = set()
        
        # Illegal keys
        for key in self.sample.keys():
            if key not in PROPERTIES_SAMPLE:
                invalids.add(key)
        
        # Required keys
        for key in REQUIRED_PROPERTIES_SAMPLE:
            if key not in self.sample.keys():
                invalids.add(key)
                
        return invalids
            
    def build(self):
        invalids = self._invalid()
        if invalids:
            raise self.ValidationError(invalids)
        return self.sample


class SampleCharacteristicsBuilder():    
    def __init__(self):
        super().__init__()
        self.characteristics = {}

    def add(self, key : str, value):
        value_type = "number"
        try:
            int(value)
        except:
            try:
                float(string)
            except:
                try:
                    complex(string)
                except:
                    value_type = "string"
                    value = str(value)
        add_dict = {
            "value": value,
            "type": value_type,
            "unit": ""
        }
        self.characteristics[key] = add_dict
        return self

    def build(self):
        return self.characteristics