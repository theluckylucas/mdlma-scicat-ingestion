from .Consts import *
from .ScanLogParser import P05LogParser
from ..Beamline.Ingestion import AbstractIngestor
from ..Beamline.ConfigKeys import *
from ...Datasets.DatasetP05 import P05RawDatasetBuilder, P05ProcessedDatasetBuilder


class P05Ingestor(AbstractIngestor):
    def __init__(self, args):
        config = {
            CONFIG_LOG_SUFFIX: LOG_SUFFIX,
            CONFIG_LOG_FILENAMES: LOG_FILENAMES,
            CONFIG_LOCATION: LOCATION,
            CONFIG_KEYWORDS: KEYWORDS,
            CONFIG_SOURCE_PATH: PATH_GPFS_P05,
            CONFIG_PREFIX: SITE_PREFIX,
            CONFIG_FILENAME_IGNORE: FILENAME_IGNORE_PATTERN,
            CONFIG_DATASET_NAME: DATASET_NAME_PATTERN
        }
        super().__init__(args, config, P05RawDatasetBuilder, P05ProcessedDatasetBuilder, P05LogParser)
    