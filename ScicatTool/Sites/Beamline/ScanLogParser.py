from abc import ABC


START_IGNORE = "****"
START_SECTION = "*** "
SEC_NAME_END = " *"
SCAN = "Start Scan"
CAM = "camera info"
APP = "apperture info"
SECTIONS = {SCAN: '=',
            CAM: ':',
            APP: '='}
SECTIONS_KEYS = [key.lower() for key in SECTIONS.keys()]
SCIENTIFIC_METADATA_KEY_FORMAT = "{} {}"
IMG_XMIN = "img_xmin"
IMG_XMAX = "img_xmax"
IMG_YMIN = "img_ymin"
IMG_YMAX = "img_ymax"


class LogParser(ABC):
    def __init__(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            self.log_dict = self._logfile_to_dict(lines)

    def _trim_line(self, line):
        return line.replace("\t", "").replace("\n", "").replace("\r", "")

    def _get_section_name(self, line):
        start = line.find(START_SECTION) + len(START_SECTION)
        end = line.find(SEC_NAME_END)
        return line[start:end]

    def _str2number(self, string):
        try:
            result = int(string)
        except:
            try:
                result = float(string)
            except:
                try:
                    result = complex(string)
                except:
                    result = string
        return result

    def _parse_section(self, section_name, lines):
        result = {}
        if section_name.lower() in SECTIONS_KEYS:
            for line in lines:
                trimed = self._trim_line(line)  # remove non-readable characters
                splits = trimed.split(SECTIONS[section_name])  # split into key and value
                if len(splits) == 2:
                    splits = [s.strip() for s in splits]  # remove surrounding whitespaces
                    key = SCIENTIFIC_METADATA_KEY_FORMAT.format(section_name, splits[0])
                    result[key] = self._str2number(splits[1])
        return result

    def _logfile_to_dict(self, lines):
        log_dict = {}
        sec_begin = 0
        sec_end = 0
        sec_start = False
        for i in range(len(lines)-1):
            if lines[i].startswith(START_IGNORE, 0, len(START_IGNORE)) and\
            lines[i+1].lower().startswith(SCAN.lower(), 0, len(SCAN)) and\
            not sec_start:
                section_name = SCAN
                sec_begin = i + 2
                sec_start = True
                continue
            elif lines[i].startswith(START_SECTION, 0, len(START_SECTION)):
                sec_end = i
                sec_dict = self._parse_section(section_name, lines[sec_begin:sec_end])
                log_dict.update(sec_dict)
                section_name = self._get_section_name(lines[i])
                sec_begin = i + 1
        if sec_start:   # last section not yet finished
            sec_dict = self._parse_section(section_name, lines[sec_begin:i])
            log_dict.update(sec_dict)
        else:
            # no proper sections detected, try to add key value pairs
            for section_name in SECTIONS.keys():
                sec_dict = self._parse_section(section_name, lines)
                log_dict.update(sec_dict)
        return log_dict

    def get_dict(self):
        return self.log_dict
