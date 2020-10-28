import xml.etree.ElementTree as ET
from copy import copy
from abc import ABC


accept = ["V80", "V91", "V110"]


class MetaParser(ABC):
    def __init__(self, filename):
        content = ""
        with open(filename, "r") as f:
            content = f.read()
        self.meta_dict = self._xml_to_dict(ET.fromstring(content))

    def _xml_to_dict(self, r, root=True):
        if root:
            return self._xml_to_dict(r, False)
        d=copy(r.attrib)
        if r.text and r.tag in accept:
            d[r.tag]=r.text
        for x in r.findall("./*"):
            d.update(self._xml_to_dict(x,False))
        return d

    def get_dict(self):
        return self.meta_dict