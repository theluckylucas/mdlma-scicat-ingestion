LOCATION = "DESY/PETRA3/P07"
SITE_PREFIX = "P07"
PATH_GPFS_P07 = "/asap3/petra3/gpfs/p07/{}/data/{}"
LOG_FILENAMES = ["beamtime-metadata-{}.json", "beamtime-metadata-{}.txt"]
LOG_SUFFIX = "scan.log"
KEYWORDS = ["synchrotron", "beamline", "xray", "HEMS"]  # Default keywords always added to any dataset beside other keywords
DATASET_NAME_PATTERN = "{}/{}/{}/{}"
FILENAME_IGNORE_PATTERN = ["_ref", "_dar"]