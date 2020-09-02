from abc import ABC, abstractmethod
import time

from .Keys import *


class DatasetBuilder(ABC):
    class ValidationError(Exception):
        MESSAGE = "Validation failed for the following properties, either missing or unknown: {}. "+\
                  "Please check scicatproject.github.io/api-documentation/ for valid keys."
        
        def __init__(self, args):
            self.args = args
            
        def __str__(self):
            return self.MESSAGE.format(', '.join(self.args))
    
    dataset = {PID: str(int(time.time() * 10000000)),
               TYPE: "base"}
    
    def args(self, args):
        return self.owner_group(args.ownergroup).\
            access_groups(args.accessgroups).\
            contact_email(args.contactemail)

    def access_groups(self, access_groups):
        self.dataset[ACCESS_GROUPS] = access_groups
        return self
    
    def owner(self, owner : str):
        self.dataset[OWNER] = owner
        return self

    def owner_group(self, owner_group : str):
        self.dataset[OWNER_GROUP] = owner_group
        return self
    
    def owner_email(self, email : str):
        self.dataset[OWNER_EMAIL] = email
        return self
    
    def contact_email(self, contact_email : str):
        self.dataset[CONTACT_EMAIL] = contact_email
        return self

    def source_folder(self, source_folder : str):
        self.dataset[SOURCE_FOLDER] = source_folder
        return self

    def source_folder_host(self, source_folder_host : str):
        self.dataset[SOURCE_FOLDER_HOST] = source_folder_host
        return self

    def size(self, size : int):
        self.dataset[SIZE] = size
        return self

    def packed_size(self, packed_size : int):
        self.dataset[PACKED_SIZE] = packed_size
        return self

    def number_of_files(self, number_of_files : int):
        self.dataset[NUMBER_OF_FILES] = number_of_files
        return self

    def number_of_files_archived(self, number_of_files_archived : int):
        self.dataset[NUMBER_OF_FILES_ARCHIVED] = number_of_files_archived
        return self

    def creation_time(self, creation_time : str):
        self.dataset[CREATION_TIME] = creation_time
        return self

    def validation_status(self, validation_status : str):
        self.dataset[VALIDATION_STATUS] = validation_status
        return self

    def keywords(self, keywords):
        self.dataset[KEYWORDS] = keywords
        return self

    def description(self, description : str):
        self.dataset[DESCRIPTION] = description
        return self

    def dataset_name(self, dataset_name : str):
        self.dataset[DATASET_NAME] = dataset_name
        return self

    def classification(self, classification : str):
        self.dataset[CLASSIFICATION] = classification
        return self

    def license(self, license : str):
        self.dataset[LICENSE] = license
        return self

    def version(self, version : str):
        self.dataset[VERSION] = version
        return self

    def is_published(self, is_published : bool):
        self.dataset[IS_PUBLISHED] = is_published
        return self

    def techniques(self, techniques):
        self.dataset[TECHNIQUES] = techniques
        return self
    
    def scientific_metadata(self, scientific_metadata):
        self.dataset[SCIENTIFIC_METADATA] = scientific_metadata
        return self

    @abstractmethod
    def _invalid(self, allowed=[], required=[]):
        invalids=set()
        
        # Illegal keys
        for key in self.dataset.keys():
            if key not in allowed:
                invalids.add(key)
        
        # Required keys
        for key in required:
            if key not in self.dataset.keys():
                invalids.add(key)
                
        return invalids
            
    def build(self):
        invalids = self._invalid()
        if invalids:
            raise self.ValidationError(invalids)
        return self.dataset
    
    
class DerivedDatasetBuilder(DatasetBuilder):
    def __init__(self):
        super().__init__()
        super().dataset[TYPE] = "derived"
        
    def investigator(self, investigator : str):
        super().dataset[INVESTIGATOR] = investigator
        return self
    
    def input_datasets(self, input_datasets):
        super().dataset[INPUT_DATASETS] = input_datasets
        return self
    
    def used_software(self, used_software):
        super().dataset[USED_SOFTWARE] = used_software
        return self
    
    def job_parameters(self, job_parameters):
        super().dataset[JOB_PARAMETERS] = job_parameters
        return self
    
    def job_log_data(self, job_log_data):
        super().dataset[JOB_LOG_DATA] = job_log_data
        return self
    
    def _invalid(self):
        return super()._invalid(PROPERTIES, REQUIRED_PROPERTIES_DATASET_BASE + REQUIRED_PROPERTIES_DATASET_DERIVED)
    
    
class RawDatasetBuilder(DatasetBuilder):
    def __init__(self):
        super().__init__()
        super().dataset[TYPE] = "raw"
        
    def principal_investigator(self, principal_investigator : str):
        super().dataset[PRINCIPAL_INVESTIGATOR] = principal_investigator
        return self
    
    def creation_location(self, creation_location : str):
        super().dataset[CREATION_LOCATION] = creation_location
        return self
    
    def end_time(self, end_time : str):
        super().dataset[END_TIME] = end_time
        return self
    
    def data_format(self, data_format):
        super().dataset[DATA_FORMAT] = data_format
        return self
    
    def _invalid(self):
        return super()._invalid(PROPERTIES, REQUIRED_PROPERTIES_DATASET_BASE + REQUIRED_PROPERTIES_DATASET_RAW)