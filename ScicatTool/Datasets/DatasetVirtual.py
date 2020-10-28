from .Dataset import DerivedDatasetBuilder
from .APIKeys import KEYWORDS as KEYWORDS_API
from .Consts import VIRTUAL_KEYWORD


def add_default_keywords(dataset_dict):
    if KEYWORDS_API in dataset_dict.keys():
        dataset_dict[KEYWORDS_API] += [VIRTUAL_KEYWORD]
    else:
        dataset_dict[KEYWORDS_API] = [VIRTUAL_KEYWORD]
    return dataset_dict


class VirtualDatasetBuilder(DerivedDatasetBuilder):
    def build(self):
        self.dataset = add_default_keywords(self.dataset)
        return super().build()