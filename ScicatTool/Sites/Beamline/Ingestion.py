from ...Proposals.Proposal import ProposalBuilder
from ...Proposals.JSONKeys import *
from ...Proposals.APIKeys import PROPOSAL_ID as PROPOSAL_ID_API
from ...Datablocks.Datablock import OrigDatablockBuilder
from ...Datablocks.APIKeys import DATA_FILE_LIST
from ...Datasets.APIKeys import PID, SOURCE_FOLDER, SIZE, ATTACHMENT_CAPTION
from ...Datasets.APIKeys import PROPOSAL_ID as PROPOSAL_ID_API_Datasets
from ...Datasets.Consts import PID_PREFIX
from ...Datasets.Dataset import AttachmentBuilder
from ...Filesystem.FSInfo import get_username, get_ownername, list_files, list_dirs, path_exists, get_creation_date, folder_total_size, get_ext
from ...Filesystem.ImInfo import get_dict_from_numpy, get_uri_from_numpy, load_numpy_from_image, TYPES, SUPPORTED_IMAGE_TYPES
from ...REST.Consts import NA
from ...REST import API
from .Consts import *
from .Keys import *

from pprint import pprint
from abc import ABC
import datetime
import json


class AbstractIngestor(ABC):
    def __init__(self, args, config, raw_dataset_builder, derived_dataset_builder, log_parser):
        super().__init__()
        self.args = args
        self.raw_dataset_builder = raw_dataset_builder
        self.derived_dataset_builder = derived_dataset_builder
        self.log_parser = log_parser
        self.config = config

    def _create_raw(self, dataset, directory, creation_time, scientific_metadata, proposal_dict):
        dataset_name = self.config[CONFIG_DATASET_NAME].format(self.config[CONFIG_PREFIX], self.args.experiment, dataset, RAW)

        images_in_folder = sorted(list_files(directory, self.args.extensions))

        total_size = folder_total_size(directory)

        dsb = self.raw_dataset_builder().\
            args(self.args).\
            proposal_id(proposal_dict[PROPOSAL_ID_API]).\
            owner(get_ownername(directory)).\
            source_folder(directory).\
            is_published(self.args.publish).\
            size(total_size).\
            principal_investigator(proposal_dict[PRINICPAL_INVESTIGATOR_LASTNAME]).\
            dataset_name(dataset_name).\
            creation_location(self.config[CONFIG_LOCATION]).\
            creation_time(creation_time).\
            scientific_metadata(scientific_metadata).\
            number_of_files(len(images_in_folder))

        return dsb.build(), images_in_folder


    def _create_derived(self, dataset, directory, subdir, postprocessing, input_datasets, binning):
        source_folder = "{}/{}".format(directory, subdir)
        images_in_folder = list_files(source_folder, self.args.extensions)
        total_size = folder_total_size(source_folder)
        investigator = get_ownername(source_folder)
        dataset_name = self.config[CONFIG_DATASET_NAME].format(self.config[CONFIG_PREFIX], self.args.experiment, dataset, postprocessing + '-' + subdir)
        creation_time = NA
        scientific_metadata = {BINNING: binning}

        if images_in_folder:
            first_image_in_folder = "{}/{}".format(source_folder, images_in_folder[0])
            creation_time = get_creation_date(source_folder)
            img_array, img_format = load_numpy_from_image(first_image_in_folder)
            if img_array is not None:
                scientific_metadata.update(get_dict_from_numpy(img_array, img_format))

        dsb = self.derived_dataset_builder().\
            args(self.args).\
            size(total_size).\
            owner(get_ownername(source_folder)).\
            source_folder(source_folder).\
            input_datasets(input_datasets).\
            is_published(self.args.publish).\
            creation_time(creation_time).\
            used_software(NA).\
            keywords([postprocessing.lower()]).\
            investigator(investigator).\
            dataset_name(dataset_name).\
            number_of_files(len(images_in_folder)).\
            scientific_metadata(scientific_metadata)

        return (dsb.build(), images_in_folder)


    def _create_proposal(self, proposal_metadata):
        pb = ProposalBuilder().\
            args(self.args).\
            proposal_id(proposal_metadata[PROPOSAL_ID]).\
            pi_email(proposal_metadata[PRINICPAL_INVESTIGATOR][PRINICPAL_INVESTIGATOR_EMAIL]).\
            pi_lastname(proposal_metadata[PRINICPAL_INVESTIGATOR][PRINICPAL_INVESTIGATOR_LASTNAME]).\
            email(proposal_metadata[APPLICANT][APPLICANT_EMAIL]).\
            lastname(proposal_metadata[APPLICANT][APPLICANT_LASTNAME]).\
            title(proposal_metadata[TITLE]).\
            start_time(proposal_metadata[EVENT_START]).\
            end_time(proposal_metadata[EVENT_END])
        return pb.build()


    def _create_origdatablock(self, filename_list, dataset_dict):
        dbb = OrigDatablockBuilder(dataset_dict[SOURCE_FOLDER]).\
            args(self.args).\
            data_file_list(filename_list).\
            size(dataset_dict[SIZE]).\
            dataset_id(dataset_dict)
        return dbb.build()


    def _create_attachments(self, filename_list, dataset_dict, proposalId):
        result = []
        failed = {}
        images_filename_list = [fn for fn in filename_list if TYPES[get_ext(fn)] in SUPPORTED_IMAGE_TYPES]
        select_filename_list = [fn for fn in images_filename_list if not any([pattern in fn for pattern in self.config[CONFIG_FILENAME_IGNORE]])]
        sorted_filename_list = sorted(select_filename_list)
        len_list = len(sorted_filename_list)
        if self.args.nattachments > 0 and len_list > 0:
            step = len_list//self.args.nattachments
            if step == 0:
                step = 1
            for i in range(0, len_list, step):
                full_path = "{}/{}".format(dataset_dict[SOURCE_FOLDER], sorted_filename_list[i])
                img_array, _ = load_numpy_from_image(full_path)
                if img_array is None:
                    failed[full_path] = "Failed to add attachment due to file format, or shape, or ..."
                else:
                    image_uri = get_uri_from_numpy(img_array, target_size=(self.args.thumbnailsize, self.args.thumbnailsize))
                    ab = AttachmentBuilder().\
                        args(self.args).\
                        thumbnail(image_uri).\
                        caption(sorted_filename_list[i]).\
                        proposal_id(proposalId)
                    result += [ab.build()]
        return result, failed


    def _api_dataset_ingest(self, dataset_dict, datablock_dict, attachment_dicts):
        failed = {}

        if not datablock_dict[DATA_FILE_LIST] and not self.args.blankdatablock:
            failed[dataset_dict[SOURCE_FOLDER]] = "No files found, thus dataset not added to Scicat!"
        else:
            # Add raw dataset
            resp = API.dataset_ingest(self.args.token, dataset_dict, self.args.simulation, self.args.verbose)
            if resp.status_code != 200:
                failed[dataset_dict[SOURCE_FOLDER]] = resp.text
            
            # Add raw dataset files
            resp = API.origdatablock_ingest(self.args.token, datablock_dict, self.args.simulation, self.args.verbose)
            if resp.status_code != 200:
                failed[dataset_dict[SOURCE_FOLDER] + "-OrigDataBlock"] = resp.text

            # Add attachments
            for attachment_dict in attachment_dicts:
                resp = API.dataset_attach(self.args.token, attachment_dict, PID_PREFIX + dataset_dict[PID], self.args.simulation, self.args.verbose)
                if resp.status_code != 200:
                    failed[attachment_dict[ATTACHMENT_CAPTION] + "-Attachment"] = resp.text

        return failed


    def _ingest_derived_dataset(self, dataset, dataset_processed_directory, subdir, postprocessing, input_datasets, proposal_dict):
        pos = subdir.rfind(RAW_BIN) + len(RAW_BIN)
        if pos == len(RAW_BIN)-1:
            pos = dataset_processed_directory.rfind(RAW_BIN) + len(RAW_BIN)
            if pos != len(RAW_BIN)-1:
                binning = int(dataset_processed_directory[pos:pos+1])
            else:
                binning = NA
        else:
            binning = int(subdir[pos:pos+1])
        dataset_dict, filename_list = self._create_derived(dataset, dataset_processed_directory, subdir, postprocessing, input_datasets, binning)
        datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
        attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_dict[PROPOSAL_ID_API])
        failed = self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts)
        failed.update(failed_attachments)
        return failed


    def _get_meta_dict(self, experiment_directory, experiment):
        for meta_log_filename in self.config[CONFIG_LOG_FILENAMES]:
            meta_path = "{}/{}".format(experiment_directory, meta_log_filename.format(experiment))
            if path_exists(meta_path):
                with open(meta_path) as json_file:
                    meta_text = json_file.read()
                pos_start = meta_text.find('{')
                pos_end = meta_text.rfind('}')
                return json.loads(meta_text[pos_start:pos_end+1])
            else:
                continue
        assert False, "Could not find proposal file in path {}".format(experiment_directory)            


    def ingest_experiment(self):
        failed = {}

        experiment_directory = self.config[CONFIG_SOURCE_PATH].format(self.args.year, self.args.experiment)

        # First, add proposal to be referred afterwards by the raw datasets
        proposal_metadata = self._get_meta_dict(experiment_directory, self.args.experiment)
        proposal_dict = self._create_proposal(proposal_metadata)
        resp = API.proposal_ingest(self.args.token, proposal_dict, self.args.simulation, self.args.verbose)
        if resp.status_code != 200:
            failed[proposal_dict[PROPOSAL_ID_API]] = resp.text

        raw_directory = "{}/{}".format(experiment_directory, RAW)
        for dataset in sorted(list_dirs(raw_directory)):
            # Include experiment metadata, and get scan parameters from log file
            # basic_metadata = {'experiment': self.args.experiment}

            dataset_raw_directory = "{}/{}".format(raw_directory, dataset)
            log_filenames = list_files(dataset_raw_directory, '.log')
            
            for log_filename in log_filenames:
                if log_filename.endswith(self.config[CONFIG_LOG_SUFFIX]):
                    path_log_filename = "{}/{}".format(dataset_raw_directory, log_filename)
                    raw_scientific_metadata = self.log_parser(path_log_filename).get_dict()
                    creation_time = get_creation_date(path_log_filename)

                    print("---*---", dataset, "---*---")

                    # Add raw dataset
                    dataset_dict, filename_list = self._create_raw(dataset, dataset_raw_directory, creation_time, raw_scientific_metadata, proposal_dict)
                    datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
                    attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_dict[PROPOSAL_ID_API])
                    failed.update(failed_attachments)
                    failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))

                    input_datasets = ["{}{}".format(PID_PREFIX, dataset_dict[PID])]  # raw dataset as input for derived datasets

                    # Add derived/processed datasets
                    for postprocessing in POSTPROCESSING:  # reco, sino, flat_corrected, phase_map, ...
                        dataset_processed_directory = "{}/{}/{}/{}".format(experiment_directory, PROCESSED, dataset, postprocessing)
                        if path_exists(dataset_processed_directory):                        # 12345678/processed/01_dataset/reco/
                            for subdir in list_dirs(dataset_processed_directory):
                                if postprocessing == RECO_PHASE:                            # 12345678/processed/01_dataset/reco/tie...
                                    dataset_tie_directory = "{}/{}".format(dataset_processed_directory, subdir)
                                    for bindir in list_dirs(dataset_tie_directory):         # 12345678/processed/01_dataset/reco/tie.../rawBin...
                                        failed.update(self._ingest_derived_dataset(dataset, dataset_tie_directory, bindir, postprocessing, input_datasets, proposal_dict))
                                elif RAW_BIN in subdir:                                     # 12345678/processed/01_dataset/reco/rawBin...
                                    if postprocessing == PHASE_MAP:
                                        dataset_rawbin_directory = "{}/{}".format(dataset_processed_directory, subdir)
                                        for tiedir in list_dirs(dataset_rawbin_directory):  # 12345678/processed/01_dataset/reco/rawBin.../tie...
                                            failed.update(self._ingest_derived_dataset(dataset, dataset_rawbin_directory, tiedir, postprocessing, input_datasets, proposal_dict))
                                    else:
                                        failed.update(self._ingest_derived_dataset(dataset, dataset_processed_directory, subdir, postprocessing, input_datasets, proposal_dict))


        if failed:    
            print("\n---!--- FAILURES ---!---")
            for key in sorted(failed.keys()):
                print(key)
                print(failed[key])
        