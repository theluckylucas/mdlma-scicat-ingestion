import argparse
from ..Datasets.APIKeys import *
from ..REST.Consts import NA


class ScicatParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("token", type=str, help="A valid SciCat token of a logged in user (see Settings)")
        self.add_argument("-v", "--verbose", type=int, choices=[0, 1, 2], default=0, help="0 = Off (default), 1 = REST request body output excl. datfiles or attachments, 2 = REST request body output incl. datafiles and attachments")
        self.add_argument("-s", "--simulation", action='store_true', help="Simulates full run, but does NOT(!) call API")

class ScicatIngestDatasetParser(ScicatParser):
    def __init__(self):
        super().__init__()
        self.add_argument("ownergroup", type=str, help=PROPERTIES[OWNER_GROUP])
        self.add_argument("contactemail", type=str, help=PROPERTIES[CONTACT_EMAIL])
        self.add_argument("-p", "--publish", action='store_true', help=PROPERTIES[IS_PUBLISHED])
        self.add_argument("-a", "--accessgroups", type=str, nargs='+', default=["public", "wb", "it", "external", "hasylab"], help=PROPERTIES[ACCESS_GROUPS])
        self.add_argument("-n", "--nattachments", type=int, default=1, help="Number of image attachments to a dataset (default: 1)")
        self.add_argument("-t", "--thumbnailsize", type=int, default=150, help="Thumbnail size (default: 150px)")
        self.add_argument("-b", "--blankdatablock", action='store_true', help="Also adds datasets without datafiles")
        self.add_argument("-k", "--keywords", type=str, nargs='+', default=[], help="Additional keywords to be added for this experiments")
        self.add_argument("-u", "--used_software", type=str, nargs='+', default=[], help="Software used for postprocessing")