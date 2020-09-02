from ..Datasets.DatasetP05 import P05RecoDatasetBuilder
from ..REST.API import *
from .Consts import *

import datetime


def ingest(args):
    scicat_token = args.token
    source_folder = PATH_GPFS_P05.format(args.year, args.experiment)
    now = str(datetime.datetime.now())
    
    investigator = "julian.moosmann@hzg.de"  # retrieve from file system
    used_software = "fiji"  # retrieve from ???
    dataset_name = "dataset" + now

    ds = P05RecoDatasetBuilder().args(args).source_folder(source_folder).input_datasets(args.inputdatasets).is_published(args.publish).creation_time(now).used_software(used_software).investigator(investigator).dataset_name(dataset_name).build()
    
    # call API to post dataset ds
    dataset_ingest(scicat_token, ds)