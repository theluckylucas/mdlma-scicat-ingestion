from .Arguments import ScicatIngestDatasetParser


DEFAULT_FILE_EXTS = [".dcm", ".hdr"]


class ZTLIngestionParser(ScicatIngestDatasetParser):
    def __init__(self):
        super().__init__()
        self.add_argument("-e", "--extensions", type=str, nargs="+", default=DEFAULT_FILE_EXTS, help="Accepted file extensions of data files (default: {})".format(DEFAULT_FILE_EXTS))

class SCAMAGIngestionParser(ScicatIngestDatasetParser):
    def __init__(self):
        super().__init__()
        self.add_argument("-e", "--extensions", type=str, nargs="+", default=DEFAULT_FILE_EXTS, help="Accepted file extensions of data files (default: {})".format(DEFAULT_FILE_EXTS))
