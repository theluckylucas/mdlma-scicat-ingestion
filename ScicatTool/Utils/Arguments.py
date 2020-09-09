import argparse
from ..Datasets.APIKeys import *


class ScicatParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("token", type=str, help="A valid SciCat token of a logged in user (see Settings)")
        self.add_argument("-v", "--verbose", type=int, choices=[0, 1, 2], default=0, help="0 = Off (default), 1 = REST request body output excl. datfiles or attachments, 2 = REST request body output incl. datafiles and attachments")
        self.add_argument("-s", "--simulation", action='store_true', help="Simulates full run, but does NOT(!) call API")
        self.add_argument("-n", "--nattach", type=int, default=1, help="Number of image attachments to a dataset")

class ScicatIngestDatasetParser(ScicatParser):
    def __init__(self):
        super().__init__()
        self.add_argument("ownergroup", type=str, help=PROPERTIES[OWNER_GROUP])
        self.add_argument("contactemail", type=str, help=PROPERTIES[CONTACT_EMAIL])
        self.add_argument("-p", "--publish", action='store_true', help=PROPERTIES[IS_PUBLISHED])
        self.add_argument("-a", "--accessgroups", type=str, nargs='+', default=["public"], help=PROPERTIES[ACCESS_GROUPS])