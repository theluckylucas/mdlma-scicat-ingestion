from ..Datasets.DatasetP05 import P05RecoDatasetBuilder
from ..Filesystem.Information import current_username, file_ownername, first_file
from ..REST.API import dataset_ingest
from .Consts import *

from pprint import pprint
import datetime


def ingest_derived(args):
    scicat_token = args.token
    now = str(datetime.datetime.now())

    data_type = RAW_BIN.format(args.rawbin)
    source_folder = PATH_GPFS_P05.format(args.year,
                                         args.experiment,
                                         "processed",
                                         args.dataset,
                                         args.reconstruction,
                                         args.datatype,
                                         data_type)
    ff = "{}/{}".format(source_folder, first_file(source_folder))
    
    dataset_name = "{}_{}_{}".format(__name__.split('.')[-2],
                                     args.experiment,
                                     args.dataset)

    dsb = P05RecoDatasetBuilder().\
        args(args).\
        owner(current_username()).\
        source_folder(source_folder).\
        input_datasets(args.inputdatasets).\
        is_published(args.publish).\
        creation_time(now).\
        used_software("n/a").\
        investigator(file_ownername(ff)).\
        dataset_name(dataset_name)

    pprint(dsb.build())
    dataset_ingest(scicat_token, dsb.build())