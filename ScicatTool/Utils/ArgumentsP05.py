from .Arguments import ScicatIngestDatasetParser
from ..Datasets.Keys import *


class P05ExperimentParser(ScicatIngestDatasetParser):
    def __init__(self):
        super().__init__()
        self.add_argument("experiment", type=int, help="an integer for the P05 experiment ID")
        self.add_argument("year", type=int, help="an integer for the year when the experiment was conducted")
        self.add_argument("dataset", type=str, help="name of the sub-directory within the experiment folder")
    
        
class P05RawExperimentParser(P05ExperimentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("-r", "--reconstruction", choices=["raw"], default="raw", help="state of reconstruction")


class P05DerivedExperimentParser(P05ExperimentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("reconstruction", type=str, choices=["sino", "reco"], help="state of reconstruction")
        self.add_argument("inputdatasets", type=str, nargs="+", help=PROPERTIES[INPUT_DATASETS])
        self.add_argument("rawbin", type=int, choices=[2, 4], help="binning of raw data for reconstruction")
        self.add_argument("-d", "--datatype", type=str, choices=["float"], default="float", help="data type")