from .Arguments import ScicatIngestDatasetParser
from ..Datasets.Keys import *


class P05ExperimentParser(ScicatIngestDatasetParser):
    def __init__(self):
        super().__init__()
        self.add_argument("experiment", type=int, help="an integer for the P05 experiment ID")
        self.add_argument("year", type=int, help="an integer for the year when the experiment was conducted")
    
        
class P05RawExperimentParser(P05ExperimentParser):
    def __init__(self):
        super().__init__()


class P05DerivedExperimentParser(P05ExperimentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("inputdatasets", type=str, nargs="+", help=PROPERTIES[INPUT_DATASETS])