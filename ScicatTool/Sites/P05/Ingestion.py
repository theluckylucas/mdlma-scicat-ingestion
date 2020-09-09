from ...Proposals.Proposal import ProposalBuilder
from ...Proposals.JSONKeys import *
from ...Proposals.APIKeys import PROPOSAL_ID as PROPOSAL_ID_API
from ...Datablocks.Datablock import OrigDatablockBuilder
from ...Datablocks.APIKeys import DATA_FILE_LIST
from ...Datasets.APIKeys import PID, SOURCE_FOLDER, SIZE, ATTACHMENT_CAPTION
from ...Datasets.APIKeys import PROPOSAL_ID as PROPOSAL_ID_API_Datasets
from ...Datasets.Consts import PID_PREFIX
from ...Datasets.Dataset import AttachmentBuilder
from ...Datasets.DatasetP05 import P05RawDatasetBuilder, P05ProcessedDatasetBuilder
from ...Filesystem.FSInfo import get_username, get_ownername, list_files, list_dirs, path_exists, get_creation_date, folder_total_size
from ...Filesystem.ImInfo import get_tif_info_dict, get_uri_from_tif
from ...REST.Consts import NA
from ...REST import API
from .Consts import *
from .ScanLog import logfile_to_dict

from pprint import pprint
import datetime
import json


def create_raw(args, dataset, directory, creation_time, scientific_metadata, proposal_dict):
    dataset_name = "{}/{}/{}-raw".format(P05_PREFIX, args.experiment, dataset)

    tiff_in_folder = sorted(list_files(directory, args.extensions))

    total_size = folder_total_size(directory)

    dsb = P05RawDatasetBuilder().\
        args(args).\
        proposal_id(proposal_dict[PROPOSAL_ID_API]).\
        owner(get_ownername(directory)).\
        source_folder(directory).\
        is_published(args.publish).\
        size(total_size).\
        principal_investigator(proposal_dict[PRINICPAL_INVESTIGATOR_LASTNAME]).\
        dataset_name(dataset_name).\
        creation_location(LOCATION).\
        creation_time(creation_time).\
        scientific_metadata(scientific_metadata).\
        number_of_files(len(tiff_in_folder))

    return dsb.build(), tiff_in_folder


def create_derived(args, dataset, directory, subdir, postprocessing, input_datasets, binning):
    source_folder = "{}/{}".format(directory, subdir)
    tiff_in_folder = list_files(source_folder, args.extensions)
    total_size = folder_total_size(source_folder)
    investigator = get_ownername(source_folder)
    dataset_name = "{}/{}/{}-{}-{}".format(P05_PREFIX, args.experiment, dataset, postprocessing, subdir)
    creation_time = NA
    scientific_metadata = {BINNING: binning}

    if tiff_in_folder:
        first_tiff_in_folder = "{}/{}".format(source_folder, tiff_in_folder[0])
        creation_time = get_creation_date(source_folder)
        scientific_metadata.update(get_tif_info_dict(first_tiff_in_folder))

    dsb = P05ProcessedDatasetBuilder().\
        args(args).\
        size(total_size).\
        owner(get_ownername(source_folder)).\
        source_folder(source_folder).\
        input_datasets(input_datasets).\
        is_published(args.publish).\
        creation_time(creation_time).\
        used_software(NA).\
        keywords([postprocessing.lower()]).\
        investigator(investigator).\
        dataset_name(dataset_name).\
        number_of_files(len(tiff_in_folder)).\
        scientific_metadata(scientific_metadata)

    return (dsb.build(), tiff_in_folder)


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


def create_attachments(args, filename_list, dataset_dict, proposalId):
    result = []
    sorted_filename_list = sorted(filename_list)
    len_list = len(filename_list)
    if args.nattachments > 0 and len_list > 0:
        step = len_list//args.nattachments
        if step == 0:
            step = 1
        for i in range(0, len_list, step):
            full_path = "{}/{}".format(dataset_dict[SOURCE_FOLDER], sorted_filename_list[i])
            ab = AttachmentBuilder().\
                args(args).\
                thumbnail(get_uri_from_tif(full_path, target_size=(args.thumbnailsize, args.thumbnailsize))).\
                caption(sorted_filename_list[i]).\
                proposal_id(proposalId)
            result += [ab.build()]
    return result


def api_dataset_ingest(args, dataset_dict, datablock_dict, attachment_dicts):
    failed = {}

    if not datablock_dict[DATA_FILE_LIST] and not args.emptyadd:
        failed[dataset_dict[SOURCE_FOLDER]] = "No files found, thus dataset not added to Scicat!"
    else:
        # Add raw dataset
        resp = API.dataset_ingest(args.token, dataset_dict, args.simulation, args.verbose)
        if resp.status_code != 200:
            failed[dataset_dict[SOURCE_FOLDER]] = resp.text
        
        # Add raw dataset files
        resp = API.origdatablock_ingest(args.token, datablock_dict, args.simulation, args.verbose)
        if resp.status_code != 200:
            failed[dataset_dict[SOURCE_FOLDER] + "-OrigDataBlock"] = resp.text

        # Add attachments
        for attachment_dict in attachment_dicts:
            resp = API.dataset_attach(args.token, attachment_dict, PID_PREFIX + dataset_dict[PID], args.simulation, args.verbose)
            if resp.status_code != 200:
                failed[attachment_dict[ATTACHMENT_CAPTION] + "-Attachment"] = resp.text

    return failed


def ingest_derived_dataset(args, dataset, dataset_processed_directory, subdir, postprocessing, input_datasets, proposal_dict):
    pos = subdir.rfind(RAW_BIN) + len(RAW_BIN)
    if pos == len(RAW_BIN)-1:
        pos = dataset_processed_directory.rfind(RAW_BIN) + len(RAW_BIN)
        if pos != len(RAW_BIN)-1:
            binning = int(dataset_processed_directory[pos:pos+1])
        else:
            binning = NA
    else:
        binning = int(subdir[pos:pos+1])
    dataset_dict, filename_list = create_derived(args, dataset, dataset_processed_directory, subdir, postprocessing, input_datasets, binning)
    datablock_dict = create_origdatablock(args, filename_list, dataset_dict)
    attachment_dicts = create_attachments(args, filename_list, dataset_dict, proposal_dict[PROPOSAL_ID_API])
    return api_dataset_ingest(args, dataset_dict, datablock_dict, attachment_dicts)


def ingest_experiment(args):
    failed = {}

    scicat_token = args.token

    experiment_directory = PATH_GPFS_P05.format(args.year, args.experiment)
    with open("{}/{}".format(experiment_directory, JSON_META_EXP.format(args.experiment))) as json_file:
        proposal_metadata = json.load(json_file)

        # First, add proposal to be referred afterwards
        proposal_dict = create_proposal(args, proposal_metadata)
        resp = API.proposal_ingest(scicat_token, proposal_dict, args.simulation, args.verbose)
        if resp.status_code != 200:
            failed[proposal_dict[PROPOSAL_ID_API]] = resp.text

    raw_directory = "{}/{}".format(experiment_directory, RAW)
    for dataset in sorted(list_dirs(raw_directory)):
        # Include experiment metadata, and get scan parameters from log file
        # basic_metadata = {'experiment': args.experiment}

        dataset_raw_directory = "{}/{}".format(raw_directory, dataset)
        log_filenames = list_files(dataset_raw_directory, '.log')
        
        for log_filename in log_filenames:
            if log_filename.endswith(LOG_SUFFIX):
                path_log_filename = "{}/{}".format(dataset_raw_directory, log_filename)
                scientific_metadata = logfile_to_dict(path_log_filename)
                creation_time = get_creation_date(path_log_filename)

                print("---*---", dataset, "---*---")

                # Add raw dataset
                dataset_dict, filename_list = create_raw(args, dataset, dataset_raw_directory, creation_time, scientific_metadata, proposal_dict)
                datablock_dict = create_origdatablock(args, filename_list, dataset_dict)
                attachment_dicts = create_attachments(args, filename_list, dataset_dict, proposal_dict[PROPOSAL_ID_API])
                failed.update(api_dataset_ingest(args, dataset_dict, datablock_dict, attachment_dicts))

                input_datasets = ["{}{}".format(PID_PREFIX, dataset_dict[PID])]  # raw dataset as input for derived datasets

                # Add derived/processed datasets
                for postprocessing in POSTPROCESSING:  # reco, sino, flat_corrected, phase_map, ...
                    dataset_processed_directory = "{}/{}/{}/{}".format(experiment_directory, PROCESSED, dataset, postprocessing)
                    if path_exists(dataset_processed_directory):                        # 12345678/processed/01_dataset/reco/
                        for subdir in list_dirs(dataset_processed_directory):
                            if postprocessing == RECO_PHASE:                            # 12345678/processed/01_dataset/reco/tie...
                                dataset_tie_directory = "{}/{}".format(dataset_processed_directory, subdir)
                                for bindir in list_dirs(dataset_tie_directory):         # 12345678/processed/01_dataset/reco/tie.../rawBin...
                                    failed.update(ingest_derived_dataset(args, dataset, dataset_tie_directory, bindir, postprocessing, input_datasets, proposal_dict))
                            elif RAW_BIN in subdir:                                     # 12345678/processed/01_dataset/reco/rawBin...
                                if postprocessing == PHASE_MAP:
                                    dataset_rawbin_directory = "{}/{}".format(dataset_processed_directory, subdir)
                                    for tiedir in list_dirs(dataset_rawbin_directory):  # 12345678/processed/01_dataset/reco/rawBin.../tie...
                                        failed.update(ingest_derived_dataset(args, dataset, dataset_rawbin_directory, tiedir, postprocessing, input_datasets, proposal_dict))
                                else:
                                    failed.update(ingest_derived_dataset(args, dataset, dataset_processed_directory, subdir, postprocessing, input_datasets, proposal_dict))


    if failed:    
        print('---!--- API FAILURES ---!---')
        for key in sorted(failed.keys()):
            print(key)
            print(failed[key])
    