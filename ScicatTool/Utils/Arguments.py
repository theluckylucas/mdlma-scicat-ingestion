import argparse
from ..Datasets.Keys import *


class ScicatIngestDatasetParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("token", type=str, help="a string for a valid SciCat token")
        self.add_argument("owner", type=str, help="a string for a valid SciCat owner")
        self.add_argument("ownergroup", type=str, help="a string for a valid DESY group")
        self.add_argument("contactemail", type=str, help=PROPERTIES[CONTACT_EMAIL])
        self.add_argument("-p", "--publish", action='store_true', help=PROPERTIES[IS_PUBLISHED])