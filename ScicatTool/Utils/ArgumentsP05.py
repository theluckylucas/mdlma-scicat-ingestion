from .Arguments import ScicatIngestDatasetParser
from ..Datasets.Keys import *


FILE_EXTS = [".tif", ".tiff"]


class P05ExperimentParser(ScicatIngestDatasetParser):
    def __init__(self):
        super().__init__()
        self.add_argument("experiment", type=int, help="an integer for the P05 experiment ID")
        self.add_argument("year", type=int, help="an integer for the year when the experiment was conducted")
        self.add_argument("-e", "--extensions", type=str, nargs="+", default=FILE_EXTS, help="Accepted file extensions of data files (default: {})".format(FILE_EXTS))