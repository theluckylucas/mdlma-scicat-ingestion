from ..Beamline.ScanLogParser import LogParser


class P05LogParser(LogParser):
    def __init__(self, filename):
        super().__init__(filename)