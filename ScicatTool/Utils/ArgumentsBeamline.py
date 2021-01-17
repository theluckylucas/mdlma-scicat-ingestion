from .Arguments import ScicatIngestDatasetParser, ScicatParser
from ..Datasets.APIKeys import *


DEFAULT_FILE_EXTS = [".tif", ".tiff", ".img"]


class BeamlineExperimentIngestionParser(ScicatIngestDatasetParser):
    def __init__(self):
        super().__init__()
        self.add_argument("experiment", type=int, help="an integer for the beamline experiment ID")
        self.add_argument("year", type=int, help="an integer for the year when the experiment was conducted")
        self.add_argument("-e", "--extensions", type=str, nargs="+", default=DEFAULT_FILE_EXTS, help="Accepted file extensions of data files (default: {})".format(DEFAULT_FILE_EXTS))


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


class PostprocessedExperimentIngestionParser(BeamlineExperimentIngestionParser):
    def __init__(self):
        super().__init__()
        self.add_argument("beamline", type=str, default="p05", help="GPFS directory name of virtual experiment folder, like p03, p05, p07, ...")
        self.add_argument("-m", "--matchexisting", action="store_true", help="Postprocessed dataset has to match with exactly one existing SRCT reco dataset as input in Scicat")
    

class ResampledExperimentIngestionParser(PostprocessedExperimentIngestionParser):
    pass


class RegisteredHistoExperimentIngestionParser(PostprocessedExperimentIngestionParser):
    def __init__(self):
        super().__init__()
        self.add_argument("csvfile", type=str, help="CSV filename including the mapping of sample id, histo id, and SRCT experiment")


class SegmentedExperimentIngestionParser(PostprocessedExperimentIngestionParser):
    def __init__(self):
        super().__init__()
        self.add_argument("csvfile", type=str, help="CSV filename including the list of segmentation folders")
