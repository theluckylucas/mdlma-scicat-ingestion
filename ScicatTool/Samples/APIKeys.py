from ..REST.CommonKeys import *


SAMPLE_ID = "sampleId"
DESCRIPTION = "description"
SAMPLE_CHARACTERISTICS = "sampleCharacteristics"
DATASET_IDS = "datasetIds"
DATASET_ID = "datasetId"
RAW_DATASET_ID = "rawDatasetId"
DERIVED_DATASET_ID = "derivedDatasetId"
IS_PUBLISHED = "isPublished"

PROPERTIES_SAMPLE = {
    SAMPLE_ID: "string",
    DESCRIPTION: "string",
    SAMPLE_CHARACTERISTICS: "object",
    IS_PUBLISHED: "Flag is true when data are made publically available",
    DATASET_IDS: "string",
    DATASET_ID: "string",
    RAW_DATASET_ID: "string",
    DERIVED_DATASET_ID: "string",
    OWNER_GROUP: COMMON_PROPERTIES[OWNER_GROUP],
    ACCESS_GROUPS: COMMON_PROPERTIES[ACCESS_GROUPS]
}

REQUIRED_PROPERTIES_SAMPLE = [SAMPLE_ID, OWNER_GROUP]
