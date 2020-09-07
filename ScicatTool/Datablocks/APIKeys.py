from ..REST.CommonKeys import *


ID = "id"
SIZE = "size"
DATA_FILE_LIST = "dataFileList"
DATASET_ID = "datasetId"
RAW_DATASET_ID = "rawDatasetId"
DERIVED_DATASET_ID = "derivedDatasetId"

PROPERTIES_DATABLOCK = {
    ID: "ObjectID string (pattern: ^[a-fA-F\d]{24}$)",
    SIZE: "Total size in bytes of all files contained in the dataFileList",
    DATA_FILE_LIST: "List of files contained in the linked dataset. Files can be regular files, folders and softlinks. All file paths are relative paths with respect to the sourceFolder location of the linked dataset.",
    DATASET_ID: "string",
    RAW_DATASET_ID: "string",
    DERIVED_DATASET_ID: "string",
    OWNER_GROUP: COMMON_PROPERTIES[OWNER_GROUP],
    ACCESS_GROUPS: COMMON_PROPERTIES[ACCESS_GROUPS]
}

REQUIRED_PROPERTIES_DATABLOCK_BASE = [SIZE]
REQUIRED_PROPERTIES_DATABLOCK_ORIGINAL = [DATA_FILE_LIST, OWNER_GROUP]


PATH = "path"
TIME = "time"
UID = "uid"
GID = "gid"

PROPERTIES_DATAFILE = {
    PATH: "Relative path of the file within the dataset folder",
    SIZE: "Uncompressed file size in bytes",
    TIME: "Time of file creation on disk, format according to chapter 5.6 internet date/time format in RFC 3339. Local times without timezone/offset info are automatically transformed to UTC using the timezone of the API server",
    UID: "optional: user ID name as seen on filesystem",
    GID: "optional: group ID name as seen on filesystem"
}

REQUIRED_PROPERTIES_DATAFILE = [PATH]