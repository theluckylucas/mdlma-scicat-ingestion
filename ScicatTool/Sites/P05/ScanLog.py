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


def trim_line(line):
    return line.replace("\t", "").replace("\n", "").replace("\r", "")


def get_section_name(line):
    start = line.find(START_SECTION) + len(START_SECTION)
    end = line.find(SEC_NAME_END)
    return line[start:end]


def str2number(string):
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


def parse_section(section_name, lines):
    result = {}
    if section_name.lower() in SECTIONS_KEYS:
        for line in lines:
            trimed = trim_line(line)  # remove non-readable characters
            splits = trimed.split(SECTIONS[section_name])  # split into key and value
            if len(splits) == 2:
                splits = [s.strip() for s in splits]  # remove surrounding whitespaces
                key = SCIENTIFIC_METADATA_KEY_FORMAT.format(section_name, splits[0])
                result[key] = str2number(splits[1])
    return result


def logfile_to_dict(filename):
    log_dict = {}
    with open(filename, "r") as f:
        lines = f.readlines()
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
                sec_dict = parse_section(section_name, lines[sec_begin:sec_end])
                log_dict.update(sec_dict)
                section_name = get_section_name(lines[i])
                sec_begin = i + 1
        if sec_start:   # last section not yet finished
            sec_dict = parse_section(section_name, lines[sec_begin:i])
            log_dict.update(sec_dict)
        else:
            # no proper sections detected, try to add key value pairs
            for section_name in SECTIONS.keys():
                sec_dict = parse_section(section_name, lines)
                log_dict.update(sec_dict)
    return log_dict
