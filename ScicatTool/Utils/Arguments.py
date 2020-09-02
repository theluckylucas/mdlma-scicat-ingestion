import argparse
from ..Datasets.Keys import *


class ScicatIngestDatasetParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("token", type=str, help="A valid SciCat token of a logged in user (see Settings)")
        self.add_argument("ownergroup", type=str, help=PROPERTIES[OWNER_GROUP])
        self.add_argument("contactemail", type=str, help=PROPERTIES[CONTACT_EMAIL])
        self.add_argument("-p", "--publish", action='store_true', help=PROPERTIES[IS_PUBLISHED])
        self.add_argument("-g", "--accessgroups", type=str, nargs='+', default=["public"], help=PROPERTIES[ACCESS_GROUPS])