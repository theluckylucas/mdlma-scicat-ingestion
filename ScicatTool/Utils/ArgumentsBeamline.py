from .Arguments import ScicatIngestDatasetParser, ScicatParser
from ..Datasets.APIKeys import *


FILE_EXTS = [".tif", ".tiff", ".img"]


class BeamlineExperimentIngestionParser(ScicatIngestDatasetParser):
    def __init__(self):
        super().__init__()
        self.add_argument("experiment", type=int, help="an integer for the beamline experiment ID")
        self.add_argument("year", type=int, help="an integer for the year when the experiment was conducted")
        self.add_argument("-e", "--extensions", type=str, nargs="+", default=FILE_EXTS, help="Accepted file extensions of data files (default: {})".format(FILE_EXTS))


class BeamlineExperimentDeletionParser(ScicatParser):
    def __init__(self):
        super().__init__()
        self.add_argument("experiment", type=int, help="an integer for the beamline experiment ID")
        self.add_argument("year", type=int, help="an integer for the year when the experiment was conducted")
        self.add_argument("-p", "--proposals", action="store_true", help="Also delete referred proposal")
        self.add_argument("-a", "--attachments", action="store_true", help="Also delete referred attachments")
        self.add_argument("-d", "--datablocks", action="store_true", help="Also delete referred datablocks")


class P05ExperimentIngestionParser(BeamlineExperimentIngestionParser):
    pass


class P05ExperimentDeletionParser(BeamlineExperimentDeletionParser):
    pass


class P07ExperimentIngestionParser(BeamlineExperimentIngestionParser):
    pass


class P07ExperimentDeletionParser(BeamlineExperimentDeletionParser):
    pass