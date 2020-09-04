from ..Datasets.Keys import PID
from ..Datasets.DatasetP05 import P05RawDatasetBuilder, P05ProcessedDatasetBuilder
from ..Filesystem.Information import get_username, get_ownername, list_files, list_dirs, path_exists, get_creation_date
from ..REST import API
from .Consts import *
from .ScanLog import logfile_to_dict

from pprint import pprint
import datetime


def create_raw(args, dataset, directory, creation_time, scientific_metadata):
    files_in_folder = list_files(directory, args.extensions)

    investigator = get_ownername(directory)

    dataset_name = "P05_{}_{}_raw".format(args.experiment, dataset)

    dsb = P05RawDatasetBuilder().\
        args(args).\
        owner(get_username()).\
        source_folder(directory).\
        is_published(args.publish).\
        principal_investigator(investigator).\
        dataset_name(dataset_name).\
        creation_location(LOCATION).\
        creation_time(creation_time).\
        scientific_metadata(scientific_metadata).\
        number_of_files(len(files_in_folder))

    return dsb.build()


def create_derived(args, dataset, directory, postprocessing, input_datasets):
    result = []    

    for d in list_dirs(directory):
        if RAW_BIN in d:
            pos = d.find(RAW_BIN) + len(RAW_BIN)
            binning = int(d[pos:pos+1])

            source_folder = "{}/{}".format(directory, d)
            files_in_folder = list_files(source_folder, args.extensions)

            investigator = get_ownername(source_folder)

            dataset_name = "P05_{}_{}_{}_{}".format(args.experiment, dataset, postprocessing, d)

            if files_in_folder:
                creation_time = get_creation_date("{}/{}".format(source_folder, files_in_folder[0]))
            else:
                creation_time = ""

            dsb = P05ProcessedDatasetBuilder().\
                args(args).\
                owner(get_username()).\
                source_folder(source_folder).\
                input_datasets(input_datasets).\
                is_published(args.publish).\
                creation_time(creation_time).\
                used_software("n/a").\
                keywords([postprocessing.lower()]).\
                investigator(investigator).\
                dataset_name(dataset_name).\
                number_of_files(len(files_in_folder))

            result += [dsb.build()]

    return result


def ingest_experiment(args):
    scicat_token = args.token

    experiment_directory = PATH_GPFS_P05.format(args.year, args.experiment)
    raw_directory = "{}/{}".format(experiment_directory, RAW)

    for dataset in list_dirs(raw_directory):

        # Get scan parameters from log file
        scientific_metadata = None

        dataset_raw_directory = "{}/{}".format(raw_directory, dataset)
        log_filenames = list_files(dataset_raw_directory, '.log')
        
        for log_filename in log_filenames:
            if log_filename.endswith('scan.log'):
                path_log_filename = "{}/{}".format(dataset_raw_directory, log_filename)
                scientific_metadata = logfile_to_dict(path_log_filename)
                scientific_metadata['experiment'] = args.experiment
                creation_time = get_creation_date(path_log_filename)

                # Add raw dataset
                dataset_dict = create_raw(args, dataset, dataset_raw_directory, creation_time, scientific_metadata)
                API.dataset_ingest(scicat_token, dataset_dict, args.simulation)

                input_datasets = ["{}{}".format(PID_PREFIX, dataset_dict[PID])]  # raw dataset as input for derived datasets

                # Add processed datasets
                for postprocessing in POSTPROCESSING:  # reco, sino, flat_corrected, phased ...
                    dataset_processed_directory = "{}/{}/{}/{}".format(experiment_directory, PROCESSED, dataset, postprocessing)
                    if path_exists(dataset_processed_directory):
                        dataset_dicts = create_derived(args, dataset, dataset_processed_directory, postprocessing, input_datasets)
                        for dataset_dict in dataset_dicts:  # rawBins ...
                            API.dataset_ingest(scicat_token, dataset_dict, args.simulation)
    