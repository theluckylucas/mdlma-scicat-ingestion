from ..REST.CommonKeys import *


PID = "pid"
OWNER = "owner"
OWNER_EMAIL = "ownerEmail"
CONTACT_EMAIL = "contactEmail"
SOURCE_FOLDER = "sourceFolder"
CREATION_TIME = "creationTime"
TYPE = "type"
SOURCE_FOLDER_HOST = "sourceFolderHost"
SIZE = "size"
PACKED_SIZE = "packedSize"
NUMBER_OF_FILES = "numberOfFiles"
NUMBER_OF_FILES_ARCHIVED = "numberOfFilesArchived"
VALIDATION_STATUS = "validationStatus"
KEYWORDS = "keywords"
DESCRIPTION = "description"
DATASET_NAME = "datasetName"
CLASSIFICATION = "classification"
LICENSE = "license"
VERSION = "version"
IS_PUBLISHED = "isPublished"
CREATED_BY = "createdBy"
UPDATED_BY = "updatedBy"
CREATED_AT = "createdAt"
UPDATED_AT = "updatedAt"
TECHNIQUES = "techniques"

INVESTIGATOR = "investigator"
INPUT_DATASETS = "inputDatasets"
USED_SOFTWARE = "usedSoftware"
JOB_PARAMETERS = "jobParameters"
JOB_LOG_DATA = "jobLogData"
SCIENTIFIC_METADATA = "scientificMetadata"

PRINCIPAL_INVESTIGATOR = "principalInvestigator"
CREATION_LOCATION = "creationLocation"
END_TIME = "endTime"
DATA_FORMAT = "dataFormat"

PROPOSAL_ID = "proposal_id"

PROPERTIES = {
    PID: "Persistent Identifier for datasets derived from UUIDv4 and prepended automatically by site specific PID prefix like 20.500.12345/",
    OWNER: "Owner of the data set, usually first name + lastname",
    OWNER_EMAIL: "Email of owner of the data set",
    CONTACT_EMAIL: "Email of contact person for this dataset",
    SOURCE_FOLDER: "Absolute file path on file server containing the files of this dataset, e.g. /some/path/to/sourcefolder. In case of a single file dataset, e.g. HDF5 data, it contains the path up to, but excluding the filename. Trailing slashes are removed.",
    SOURCE_FOLDER_HOST: "DNS host name of file server hosting sourceFolder, optionally including protocol e.g. [protocol://]fileserver1.example.com",
    SIZE: "Total size of all source files contained in source folder on disk when unpacked",
    PACKED_SIZE: "Total size of all datablock package files created for this dataset",
    NUMBER_OF_FILES: "Total number of lines in filelisting of all OrigDatablocks for this dataset",
    NUMBER_OF_FILES_ARCHIVED: "Total number of lines in filelisting of all Datablocks for this dataset",
    CREATION_TIME: "Time when dataset became fully available on disk, i.e. all containing files have been written. Format according to chapter 5.6 internet date/time format in RFC 3339. Local times without timezone/offset info are automatically transformed to UTC using the timezone of the API server.",
    TYPE: "Characterize type of dataset, either ‘base’ or ‘raw’ or 'derived’. Autofilled when choosing the proper inherited models",
    VALIDATION_STATUS: "Defines a level of trust, e.g. a measure of how much data was verified or used by other persons",
    KEYWORDS: "Array of tags associated with the meaning or contents of this dataset. Values should ideally come from defined vocabularies, taxonomies, ontologies or knowledge graphs",
    DESCRIPTION: "Free text explanation of contents of dataset",
    DATASET_NAME: "A name for the dataset, given by the creator to carry some semantic meaning. Useful for display purposes e.g. instead of displaying the pid. Will be autofilled if missing using info from sourceFolder",
    CLASSIFICATION: "ACIA information about AUthenticity,COnfidentiality,INtegrity and AVailability requirements of dataset. E.g. AV(ailabilty)=medium could trigger the creation of a two tape copies. Format ‘AV=medium,CO=low’",
    LICENSE: "Name of license under which data can be used",
    VERSION: "Version of API used in creation of dataset",
    IS_PUBLISHED: "Flag is true when data are made publically available",
    CREATED_BY: "Functional or user account name who created this instance",
    UPDATED_BY: "Functional or user account name who last updated this instance",
    CREATED_AT: "string($date-time)",
    UPDATED_AT: "string($date-time)",
    TECHNIQUES: "Technique type stores the metadata information for a technique",
    OWNER_GROUP: COMMON_PROPERTIES[OWNER_GROUP],
    ACCESS_GROUPS: COMMON_PROPERTIES[ACCESS_GROUPS],
    
    INVESTIGATOR: "Email of person pursuing the data analysis",
    INPUT_DATASETS: "Array of input dataset identifiers used in producing the derived dataset. Ideally these are the global identifier to existing datasets inside this or federated data catalogs",
    USED_SOFTWARE: "A list of links to software repositories which uniquely identifies the software used and the version for yielding the derived data",
    JOB_PARAMETERS: "The creation process of the drived data will usually depend on input job parameters. The full structure of these input parameters are stored here",
    JOB_LOG_DATA: "The output job logfile. Keep the size of this log data well below 15 MB",
    SCIENTIFIC_METADATA: "JSON object containing the scientific meta data",
    
    PRINCIPAL_INVESTIGATOR: "Email of principal investigator",
    CREATION_LOCATION: "Unique location identifier where data was taken, usually in the form /Site-name/facility-name/instrumentOrBeamline-name",
    END_TIME: "string($date-time) Time of end of data taking for this dataset, format according to chapter 5.6 internet date/time format in RFC 3339. Local times without timezone/offset info are automatically transformed to UTC using the timezone of the API server",
    DATA_FORMAT: "Defines format of subsequent scientific meta data, e.g Nexus Version x.y",

    PROPOSAL_ID: "Proposal ID"
}


# PID, CREATED_AT, CREATED_BY, UPDATED_AT, UPDATED_BY will be automatically assigned by Scicat API / database
REQUIRED_PROPERTIES_DATASET_BASE = [OWNER, OWNER_GROUP, ACCESS_GROUPS, CONTACT_EMAIL, SOURCE_FOLDER, CREATION_TIME, TYPE]
REQUIRED_PROPERTIES_DATASET_DERIVED = [INVESTIGATOR, INPUT_DATASETS, USED_SOFTWARE]
REQUIRED_PROPERTIES_DATASET_RAW = [PRINCIPAL_INVESTIGATOR, CREATION_LOCATION]