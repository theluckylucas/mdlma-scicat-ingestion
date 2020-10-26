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
    def __init__(self):
        super().__init__()
        self.add_argument("-r", "--rawonly", action="store_true", help="Add only raw datasets")


class P05ExperimentDeletionParser(BeamlineExperimentDeletionParser):
    pass


class P07ExperimentIngestionParser(BeamlineExperimentIngestionParser):
    def __init__(self):
        super().__init__()
        self.add_argument("-r", "--rawonly", action="store_true", help="Add only raw datasets")


class P07ExperimentDeletionParser(BeamlineExperimentDeletionParser):
    pass


class ResampledExperimentIngestionParser(BeamlineExperimentIngestionParser):
    def __init__(self):
        super().__init__()
        self.add_argument("beamline", type=str, default="p05", help="GPFS directory names, like p03, p05, p07, ...")
        self.add_argument("-m", "--matchraw", action="store_true", help="Resampled dataset has to match with exactly one existing raw dataset as input in Scicat")