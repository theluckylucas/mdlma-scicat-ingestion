from ..Proposals.Proposal import ProposalBuilder
from ..Proposals.JSONKeys import *
from ..Proposals.APIKeys import PROPOSAL_ID as PROPOSAL_ID_API
from ..Datablocks.Datablock import OrigDatablockBuilder
from ..Datasets.APIKeys import PID, SOURCE_FOLDER, SIZE
from ..Datasets.Consts import PID_PREFIX
from ..Datasets.DatasetP05 import P05RawDatasetBuilder, P05ProcessedDatasetBuilder
from ..Filesystem.FSInfo import get_username, get_ownername, list_files, list_dirs, path_exists, get_creation_date, folder_total_size
from ..Filesystem.ImInfo import get_tif_info_dict
from ..REST import API
from .Consts import *
from .ScanLog import logfile_to_dict

from pprint import pprint
import datetime
import json


def create_raw(args, dataset, directory, creation_time, scientific_metadata, proposal_dict):
    files_in_folder = list_files(directory, args.extensions)

    dataset_name = "{}/{}/{}-raw".format(P05_PREFIX, args.experiment, dataset)

    tiff_in_folder = list_files(directory, args.extensions)

    total_size = folder_total_size(directory)

    dsb = P05RawDatasetBuilder().\
        args(args).\
        proposal_id(proposal_dict[PROPOSAL_ID_API]).\
        owner(get_username()).\
        source_folder(directory).\
        is_published(args.publish).\
        size(total_size).\
        principal_investigator(proposal_dict[PRINICPAL_INVESTIGATOR_LASTNAME]).\
        dataset_name(dataset_name).\
        creation_location(LOCATION).\
        creation_time(creation_time).\
        scientific_metadata(scientific_metadata).\
        number_of_files(len(files_in_folder))

    return dsb.build(), tiff_in_folder


def create_derived(args, dataset, directory, postprocessing, input_datasets):
    result = []

    for d in list_dirs(directory):
        if RAW_BIN in d:
            pos = d.find(RAW_BIN) + len(RAW_BIN)
            binning = int(d[pos:pos+1])

            source_folder = "{}/{}".format(directory, d)
            tiff_in_folder = list_files(source_folder, args.extensions)

            total_size = folder_total_size(source_folder)

            investigator = get_ownername(source_folder)

            dataset_name = "{}/{}/{}-{}-{}".format(P05_PREFIX, args.experiment, dataset, postprocessing, d)

            if tiff_in_folder:
                first_tiff_in_folder = "{}/{}".format(source_folder, tiff_in_folder[0])
                creation_time = get_creation_date(first_tiff_in_folder)
                scientific_metadata = get_tif_info_dict(first_tiff_in_folder)
            else:
                creation_time = "NO FILES CREATED"
                scientific_metadata = {}

            dsb = P05ProcessedDatasetBuilder().\
                args(args).\
                size(total_size).\
                owner(get_username()).\
                source_folder(source_folder).\
                input_datasets(input_datasets).\
                is_published(args.publish).\
                creation_time(creation_time).\
                used_software("n/a").\
                keywords([postprocessing.lower()]).\
                investigator(investigator).\
                dataset_name(dataset_name).\
                number_of_files(len(tiff_in_folder)).\
                scientific_metadata(scientific_metadata)

            result += [(dsb.build(), tiff_in_folder)]

    return result


def create_proposal(args, proposal_metadata):
    pb = ProposalBuilder().\
        args(args).\
        proposal_id(proposal_metadata[PROPOSAL_ID]).\
        pi_email(proposal_metadata[PRINICPAL_INVESTIGATOR][PRINICPAL_INVESTIGATOR_EMAIL]).\
        pi_lastname(proposal_metadata[PRINICPAL_INVESTIGATOR][PRINICPAL_INVESTIGATOR_LASTNAME]).\
        email(proposal_metadata[APPLICANT][APPLICANT_EMAIL]).\
        lastname(proposal_metadata[APPLICANT][APPLICANT_LASTNAME]).\
        title(proposal_metadata[TITLE]).\
        start_time(proposal_metadata[EVENT_START]).\
        end_time(proposal_metadata[EVENT_END])
    return pb.build()


def create_origdatablock(args, filename_list, dataset_dict):
    dbb = OrigDatablockBuilder(dataset_dict[SOURCE_FOLDER]).\
        args(args).\
        data_file_list(filename_list).\
        size(dataset_dict[SIZE]).\
        dataset_id(dataset_dict)
    return dbb.build()


def ingest_experiment(args):
    failed = {}

    scicat_token = args.token

    experiment_directory = PATH_GPFS_P05.format(args.year, args.experiment)
    with open("{}/{}".format(experiment_directory, JSON_META_EXP.format(args.experiment))) as json_file:
        proposal_metadata = json.load(json_file)

        # First, add proposal to be referred afterwards
        proposal_dict = create_proposal(args, proposal_metadata)
        resp = API.proposal_ingest(scicat_token, proposal_dict, args.simulation)
        if resp.status_code != 200:
            failed[proposal_dict[PROPOSAL_ID_API]] = resp.text

    raw_directory = "{}/{}".format(experiment_directory, RAW)

    for dataset in list_dirs(raw_directory):

        # Include experiment metadata, and get scan parameters from log file
        scientific_metadata = {
            TITLE: proposal_dict[TITLE],
        }

        dataset_raw_directory = "{}/{}".format(raw_directory, dataset)
        log_filenames = list_files(dataset_raw_directory, '.log')
        
        for log_filename in log_filenames:
            if log_filename.endswith(LOG_SUFFIX):
                path_log_filename = "{}/{}".format(dataset_raw_directory, log_filename)
                scientific_metadata = logfile_to_dict(path_log_filename)
                scientific_metadata['experiment'] = args.experiment
                creation_time = get_creation_date(path_log_filename)

                # Add raw dataset
                dataset_dict, filename_list = create_raw(args, dataset, dataset_raw_directory, creation_time, scientific_metadata, proposal_dict)
                resp = API.dataset_ingest(scicat_token, dataset_dict, args.simulation)
                if resp.status_code != 200:
                    failed[dataset_dict[SOURCE_FOLDER]] = resp.text
                
                # Add raw dataset files
                datablock_dict = create_origdatablock(args, filename_list, dataset_dict)
                resp = API.origdatablock_ingest(scicat_token, datablock_dict, args.simulation)
                if resp.status_code != 200:
                    failed[dataset_dict[SOURCE_FOLDER] + "-OrigDataBlock"] = resp.text

                input_datasets = ["{}{}".format(PID_PREFIX, dataset_dict[PID])]  # raw dataset as input for derived datasets

                # Add processed datasets
                for postprocessing in POSTPROCESSING:  # reco, sino, flat_corrected, phased ...
                    dataset_processed_directory = "{}/{}/{}/{}".format(experiment_directory, PROCESSED, dataset, postprocessing)
                    if path_exists(dataset_processed_directory):
                        derived_datasets = create_derived(args, dataset, dataset_processed_directory, postprocessing, input_datasets)
                        for dataset_dict, filename_list in derived_datasets:

                            # Add derived dataset
                            resp = API.dataset_ingest(scicat_token, dataset_dict, args.simulation)
                            if resp.status_code != 200:
                                failed[dataset_dict[SOURCE_FOLDER]] = resp.text

                            # Add derived datasets' files
                            datablock_dict = create_origdatablock(args, filename_list, dataset_dict)
                            resp = API.origdatablock_ingest(scicat_token, datablock_dict, args.simulation)
                            if resp.status_code != 200:
                                failed[dataset_dict[SOURCE_FOLDER] + "-OrigDataBlock"] = resp.text

    if failed:    
        print('---!--- API FAILURES ---!---')
        for key, value in failed.items():
            print(key)
            print(value)
    