from .Dataset import DerivedDatasetBuilder, RawDatasetBuilder
from .APIKeys import KEYWORDS as KEYWORDS_API
from ..Sites.P07.Consts import KEYWORDS as KEYWORDS_P07


def add_default_keywords(dataset_dict):
    if KEYWORDS_API in dataset_dict.keys():
        dataset_dict[KEYWORDS_API] += KEYWORDS_P07
    else:
        dataset_dict[KEYWORDS_API] = KEYWORDS_P07
    return dataset_dict


class P07RawDatasetBuilder(RawDatasetBuilder):
    def build(self):
        self.dataset = add_default_keywords(self.dataset)
        return super().build()
    
class P07ProcessedDatasetBuilder(DerivedDatasetBuilder):
    def build(self):
        self.dataset = add_default_keywords(self.dataset)
        return super().build()