from .Dataset import DerivedDatasetBuilder, RawDatasetBuilder
from .APIKeys import KEYWORDS as KEYWORDS_API
from .Consts import VIRTUAL_KEYWORD, HISTO_KEYWORD


def add_default_keywords(dataset_dict, keywords):
    if KEYWORDS_API in dataset_dict.keys():
        dataset_dict[KEYWORDS_API] += keywords
    else:
        dataset_dict[KEYWORDS_API] = keywords
    return dataset_dict


class HistoRawDatasetBuilder(RawDatasetBuilder):
    def build(self):
        self.dataset = add_default_keywords(self.dataset, [HISTO_KEYWORD])
        return super().build()


class VirtualDatasetBuilder(DerivedDatasetBuilder):
    def build(self):
        self.dataset = add_default_keywords(self.dataset, [VIRTUAL_KEYWORD])
        return super().build()