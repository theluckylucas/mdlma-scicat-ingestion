
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


def trim_line(line):
    return line.replace("\t", "").replace(" ", "")


def get_section_name(line):
    start = line.find(START_SECTION) + len(START_SECTION)
    end = line.find(SEC_NAME_END)
    return line[start:end]


def parse_section(log_dict, section_name, lines):
    if section_name.lower() in SECTIONS_KEYS:
        for line in lines:
            trimed = trim_line(line)
            splits = trimed.split(SECTIONS[section_name])
            if len(splits) == 2:
                key = "{} {}".format(section_name, splits[0])
                log_dict[key] = splits[1]
    return log_dict


def logfile_to_dict(filename):
    log_dict = {}
    with open(filename, "r") as f:
        lines = f.readlines()
        sec_begin = 0
        sec_end = 0
        sec_start = False
        for i, line in enumerate(lines):
            if line.startswith(START_IGNORE, 0, len(START_IGNORE)) and\
               lines[i+1].lower().startswith(SCAN.lower(), 0, len(SCAN)) and\
               not sec_start:
                section_name = SCAN
                sec_begin = i + 2
                sec_start = True
                continue
            elif line.startswith(START_SECTION, 0, len(START_SECTION)):
                sec_end = i
                sec_dict = parse_section(log_dict, section_name, lines[sec_begin:sec_end])
                log_dict = {**log_dict, **sec_dict}
                section_name = get_section_name(line)
                sec_begin = i + 1
        log_dict = parse_section(log_dict, section_name, lines[sec_begin:i])  # last section not yet finished
    return log_dict
