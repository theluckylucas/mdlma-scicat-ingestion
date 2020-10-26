from .Consts import *
from .ScanLogParser import P07LogParser
from ..Beamline.Ingestion import AbstractIngestor
from ..Beamline.ConfigKeys import *
from ...Datasets.DatasetP07 import P07RawDatasetBuilder, P07ProcessedDatasetBuilder


class P07Ingestor(AbstractIngestor):
    def __init__(self, args):
        config = {
            CONFIG_LOG_SUFFIX: LOG_SUFFIX,
            CONFIG_LOG_FILENAMES: LOG_FILENAMES,
            CONFIG_LOCATION: LOCATION,
            CONFIG_KEYWORDS: KEYWORDS,
            CONFIG_SOURCE_PATH: PATH_GPFS_P07,
            CONFIG_PREFIX: SITE_PREFIX,
            CONFIG_FILENAME_IGNORE: FILENAME_IGNORE_PATTERN,
            CONFIG_DATASET_NAME: DATASET_NAME_PATTERN
        }
        super().__init__(args, config, P07RawDatasetBuilder, P07ProcessedDatasetBuilder, P07LogParser)
    