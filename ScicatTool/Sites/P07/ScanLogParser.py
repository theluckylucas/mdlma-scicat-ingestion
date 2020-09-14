from ..Beamline.ScanLogParser import LogParser


class P07LogParser(LogParser):
    def __init__(self, filename):
        super().__init__(filename)