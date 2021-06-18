from .Dataset import DerivedDatasetBuilder, RawDatasetBuilder


class HistoRawDatasetBuilder(RawDatasetBuilder):
    pass


class HistoRegistedDatasetBuilder(DerivedDatasetBuilder):
    pass


class ResampledDatasetBuilder(DerivedDatasetBuilder):
    pass


class SegmentedDatasetBuilder(DerivedDatasetBuilder):
    pass


class ZTLMRDatasetBuilder(RawDatasetBuilder):
    pass


class ZTLCTDatasetBuilder(RawDatasetBuilder):
    pass


class SCAMAGDatasetBuilder(RawDatasetBuilder):
    pass