from ..Beamline.XMLMetaParser import MetaParser 


class HistoMetaParser(MetaParser):
    def __init__(self, filename):
        super().__init__(filename)