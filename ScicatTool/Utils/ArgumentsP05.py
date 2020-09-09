from .Arguments import ScicatIngestDatasetParser, ScicatParser
from ..Datasets.APIKeys import *


FILE_EXTS = [".tif", ".tiff"]


class P05ExperimentIngestionParser(ScicatIngestDatasetParser):
    def __init__(self):
        super().__init__()
        self.add_argument("experiment", type=int, help="an integer for the P05 experiment ID")
        self.add_argument("year", type=int, help="an integer for the year when the experiment was conducted")
        self.add_argument("-e", "--extensions", type=str, nargs="+", default=FILE_EXTS, help="Accepted file extensions of data files (default: {})".format(FILE_EXTS))


class P05ExperimentDeletionParser(ScicatParser):
    def __init__(self):
        super().__init__()
        self.add_argument("experiment", type=int, help="an integer for the P05 experiment ID")
        self.add_argument("year", type=int, help="an integer for the year when the experiment was conducted")
        self.add_argument("-d", "--delpro", action="store_true", help="Also delete referred proposal")