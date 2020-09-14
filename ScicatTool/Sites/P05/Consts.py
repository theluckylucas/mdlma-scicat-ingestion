LOCATION = "DESY/PETRA3/P05"
SITE_PREFIX = "P05"
PATH_GPFS_P05 = "/asap3/petra3/gpfs/p05/{}/data/{}"
LOG_FILENAMES = ["beamtime-metadata-{}.json", "beamtime-metadata-{}.txt"]
LOG_SUFFIX = "scan.log"
KEYWORDS = ["synchrotron", "beamline", "xray", "IBL", "tomography"]  # Default keywords always added to any dataset beside other keywords
DATASET_NAME_PATTERN = "{}/{}/{}/{}"
FILENAME_IGNORE_PATTERN = ["_ref", "_dar"]