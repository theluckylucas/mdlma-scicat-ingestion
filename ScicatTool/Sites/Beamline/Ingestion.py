from ...Proposals.Proposal import ProposalBuilder
from ...Proposals.JSONKeys import *
from ...Proposals.APIKeys import PROPOSAL_ID as PROPOSAL_ID_API
from ...Datablocks.Datablock import OrigDatablockBuilder
from ...Datablocks.APIKeys import DATA_FILE_LIST
from ...Datasets.APIKeys import PID, SOURCE_FOLDER, SIZE, ATTACHMENT_CAPTION
from ...Datasets.APIKeys import PROPOSAL_ID as PROPOSAL_ID_API_Datasets
from ...Datasets.Consts import PID_PREFIX
from ...Datasets.Dataset import AttachmentBuilder, ScientificMetadataBuilder
from ...Filesystem.FSInfo import get_username, get_ownername, list_files, list_dirs, path_exists, get_creation_date, folder_total_size, get_ext
from ...Filesystem.ImInfo import get_dict_from_numpy, get_uri_from_numpy, load_numpy_from_image, TYPES, SUPPORTED_IMAGE_TYPES
from ...REST.Consts import NA
from ...REST import API
from .Consts import *
from .ConfigKeys import *

from pprint import pprint
from abc import ABC
import datetime
import json
import re


class AbstractIngestor(ABC):
    def __init__(self, args, config, raw_dataset_builder, derived_dataset_builder, log_parser):
        super().__init__()
        self.args = args
        self.raw_dataset_builder = raw_dataset_builder
        self.derived_dataset_builder = derived_dataset_builder
        self.log_parser = log_parser
        self.config = config

    def _sample_id_from_dataset_name(self, dataset_name):
        sample_id_pattern_match = re.findall("_\d+[a-zA-Z]+_", dataset_name)
        if len(sample_id_pattern_match) == 1:
            sample_id = sample_id_pattern_match[0][1:-1]
            if len(sample_id) < 6:
                return sample_id
        return None


    def dataset_raw_name(self, pattern, prefix, experiment_id, dataset, post_processing, histo_id):
        return pattern.format(prefix, experiment_id, dataset, post_processing)


    def _create_raw(self, dataset, directory, creation_time, scientific_metadata, proposal_dict, sample_id, prefix, histo_id):
        dataset_name = self.dataset_raw_name(self.config[CONFIG_DATASET_NAME], prefix, self.args.experiment, dataset, RAW, histo_id)

        images_in_folder = list_files(directory, self.args.extensions)
        for subdir in list_dirs(directory):
            images_in_folder += ["{}/{}".format(subdir, f) for f in list_files("{}/{}".format(directory, subdir), self.args.extensions)]
        images_in_folder = sorted(images_in_folder)

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

        if sample_id is not None:
            dsb.sample_id(sample_id)

        return dsb.build(), images_in_folder

    
    def dataset_derived_name(self, pattern, prefix, experiment_id, dataset_name, post_processing, subdir, suffix=None):
        if suffix is None:
            suffix = ""
        return pattern.format(prefix, experiment_id, dataset_name, post_processing + '-' + subdir + suffix)


    def _create_derived(self, dataset, directory, subdir, postprocessing, input_datasets, binning, site_prefix, experiment_id, suffix):
        source_folder = "{}/{}".format(directory, subdir)
        images_in_folder = list_files(source_folder, self.args.extensions)
        total_size = folder_total_size(source_folder)
        investigator = get_ownername(source_folder)
        dataset_name = self.dataset_derived_name(self.config[CONFIG_DATASET_NAME],\
                                                 site_prefix,\
                                                 experiment_id,\
                                                 dataset,\
                                                 postprocessing,\
                                                 subdir,\
                                                 suffix)
        creation_time = NA
        smb = ScientificMetadataBuilder().add(BINNING, binning)

        if images_in_folder:
            first_image_in_folder = "{}/{}".format(source_folder, images_in_folder[0])
            creation_time = get_creation_date(source_folder)
            img_array, img_format = load_numpy_from_image(first_image_in_folder)
            if img_array is not None:
                img_metadata = get_dict_from_numpy(img_array, img_format)
                for key, value in img_metadata.items():
                    smb.add(key, value)

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
            scientific_metadata(smb.build())

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
            # Add dataset
            resp = API.dataset_ingest(self.args.token, dataset_dict, self.args.simulation, self.args.verbose)
            if resp.status_code != 200:
                failed[dataset_dict[SOURCE_FOLDER]] = resp.text
            
            # Add dataset files in a OrigDatablock
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
        dataset_dict, filename_list = self._create_derived(dataset, dataset_processed_directory, subdir, postprocessing, input_datasets, binning, self.config[CONFIG_PREFIX], self.args.experiment, suffix=None)
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
            
            dataset_raw_directory = "{}/{}".format(raw_directory, dataset)
            log_filenames = list_files(dataset_raw_directory, '.log')
            
            for log_filename in log_filenames:
                if log_filename.endswith(self.config[CONFIG_LOG_SUFFIX]):
                    path_log_filename = "{}/{}".format(dataset_raw_directory, log_filename)
                    log_metadata = self.log_parser(path_log_filename).get_dict()
                    smb = ScientificMetadataBuilder()
                    for key, value in log_metadata.items():
                        smb.add(key, value)
                    creation_time = get_creation_date(path_log_filename)

                    print("=>", dataset)

                    # Add raw dataset
                    sample_id = self._sample_id_from_dataset_name(dataset)
                    dataset_dict, filename_list = self._create_raw(dataset, dataset_raw_directory, creation_time, smb.build(), proposal_dict, sample_id, self.config[CONFIG_PREFIX], None)
                    datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
                    attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_dict[PROPOSAL_ID_API])
                    failed.update(failed_attachments)
                    failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))

                    input_datasets = ["{}{}".format(PID_PREFIX, dataset_dict[PID])]  # raw dataset as input for derived datasets
                    
                    if self.args.rawonly:
                        continue

                    # Add derived/processed datasets
                    for postprocessing in POSTPROCESSING:  # reco, sino, flat_corrected, phase_map, ...
                        dataset_processed_directory = "{}/{}/{}/{}".format(experiment_directory, PROCESSED, dataset, postprocessing)
                        if path_exists(dataset_processed_directory):                        # 12345678/processed/01_dataset/reco/
                            for subdir in list_dirs(dataset_processed_directory):
                                if postprocessing == RECO_PHASE:                            # 12345678/processed/01_dataset/reco_phase/tie...
                                    dataset_tie_directory = "{}/{}".format(dataset_processed_directory, subdir)
                                    for bindir in list_dirs(dataset_tie_directory):         # 12345678/processed/01_dataset/reco_phase/tie.../rawBin...
                                        failed.update(self._ingest_derived_dataset(dataset, dataset_tie_directory, bindir, postprocessing, input_datasets, proposal_dict))
                                elif RAW_BIN in subdir:                                     # 12345678/processed/01_dataset/reco/rawBin...
                                    if postprocessing == PHASE_MAP:
                                        dataset_rawbin_directory = "{}/{}".format(dataset_processed_directory, subdir)
                                        for tiedir in list_dirs(dataset_rawbin_directory):  # 12345678/processed/01_dataset/phase_map/rawBin.../tie...
                                            failed.update(self._ingest_derived_dataset(dataset, dataset_rawbin_directory, tiedir, postprocessing, input_datasets, proposal_dict))
                                    else:                                                   # 12345678/processed/01_dataset/reco/rawBin...
                                        failed.update(self._ingest_derived_dataset(dataset, dataset_processed_directory, subdir, postprocessing, input_datasets, proposal_dict))


        if failed:    
            print("\n---!--- FAILURES ---!---")
            for key in sorted(failed.keys()):
                print("\n=>", key, "\n", failed[key], "\n")
        