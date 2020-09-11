from .Consts import *
from .LogParser import P05LogParser
from ..Ingestion.Ingestion import AbstractIngestor
from ..Ingestion.Keys import *
from ...Datasets.DatasetP05 import P05RawDatasetBuilder, P05ProcessedDatasetBuilder


class P05Ingestor(AbstractIngestor):
    def __init__(self, args):
        config = {
            CONFIG_LOG_SUFFIX: LOG_SUFFIX,
            CONFIG_LOG_FILENAMES: LOG_FILENAMES,
            CONFIG_LOCATION: LOCATION,
            CONFIG_KEYWORDS: KEYWORDS,
            CONFIG_SOURCE_PATH: PATH_GPFS_P05,
            CONFIG_PREFIX: SITE_PREFIX
        }
        super().__init__(args, config, P05RawDatasetBuilder, P05ProcessedDatasetBuilder, P05LogParser)
    