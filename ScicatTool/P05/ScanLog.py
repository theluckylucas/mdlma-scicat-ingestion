
START_IGNORE = "****"
START_SECTION = "*** "
SEC_NAME_END = " *"
SCAN = "Start Scan"
FOV = "Field of info"
APP = "apperture info"
SECTIONS = {SCAN: '=',
            FOV: ':',
            APP: '='}


def trim_line(line):
    return line.replace("\t", "").replace(" ", "")


def get_section_name(line):
    start = line.find(START_SECTION) + len(START_SECTION)
    end = line.find(SEC_NAME_END)
    return line[start:end]


def parse_section(log_dict, lines):
    section_name = get_section_name(lines[0])
    for i in range(1, len(lines)):
        if section_name in SECTIONS:
            key, value = trim_line(lines[i]).split(SECTIONS[section_name])
            key_dict = "{}: {}".format(section_name, key)
            log_dict[key_dict] = value
    return log_dict


def logfile_to_dict(filename):
    log_dict = {}
    with open(filename, "r") as f:
        lines = f.readlines()
        sec_begin = 0
        sec_end = 0
        sec_process = False
        for i, line in enumerate(lines):
            if line.startswith(START_IGNORE, 0, len(START_IGNORE)):
                continue
            elif line.startswith(START_SECTION, 0, len(START_SECTION)):
                if sec_process:
                    sec_end = i
                    log_dict = parse_section(log_dict, lines[sec_begin:sec_end])
                    sec_process = False
                else:
                    sec_begin = i
                    sec_process = True
                    continue
        if sec_process:
            log_dict = parse_section(log_dict, lines[sec_begin:i])
    return log_dict
