from ...Proposals.Proposal import ProposalBuilder
from ...Proposals.APIKeys import PROPOSAL_ID as PROPOSAL_ID_API
from ...Proposals.APIKeys import PI_LASTNAME
from .Consts import *
from ..Beamline.Ingestion import AbstractIngestor
from ..Beamline.ConfigKeys import *
from ..Beamline.Consts import RAW
from ...Datasets.DatasetVirtual import ZTLCTDatasetBuilder
from ...Datasets.APIKeys import SOURCE_FOLDER
from ...Filesystem.FSInfo import list_dirs, list_files, get_creation_date, folder_total_size
from ...Filesystem.FSInfoUnix import get_ownername
from ...Filesystem.ImInfo import load_numpy_from_image
from ...Datasets.Dataset import AttachmentBuilder, ScientificMetadataBuilder
from ...REST.Consts import NA
from ...REST import API


class ZTLCTIngestor(AbstractIngestor):
    def __init__(self, args):
        config = {
            CONFIG_LOG_SUFFIX: LOG_SUFFIX,
            CONFIG_LOG_FILENAMES: LOG_FILENAMES,
            CONFIG_LOCATION: LOCATION,
            CONFIG_KEYWORDS: KEYWORDS,
            CONFIG_SOURCE_PATH: SOURCE_PATH,
            CONFIG_PREFIX: SITE_PREFIX,
            CONFIG_FILENAME_IGNORE: FILENAME_IGNORE_PATTERN,
            CONFIG_DATASET_NAME: DATASET_CT_NAME_PATTERN
        }
        super().__init__(args, config, ZTLCTDatasetBuilder, None, None)


    def _create_raw(self, dataset, directory, creation_time, smb, proposal_dict, sample_id, prefix, histo_id):

        smb.set_value("Day after implant", DAY_POST_SACRIFICE)

        images_in_folder = sorted(list_files(directory, self.args.extensions))
        
        meta_info_file = "{}/{}".format(directory, images_in_folder[0])
        creation_time = get_creation_date(meta_info_file)
        _, _, dicom_meta = load_numpy_from_image(meta_info_file)
        for tag in DICOM_TAGS_CT:
            value = dicom_meta.get(tag, NA)
            if isinstance(value, list):
                value = ",".join([str(v) for v in value])
            smb.set_value("DICOM_" + tag, value)

        smb.set_value("Date of Image", dicom_meta.get("StudyDate", NA))

        sample_id = dicom_meta.get("PatientID", None)
        if sample_id is not None:
            sample_id = sample_id[:5]

        total_size = folder_total_size(directory)

        dataset_name = self.config[CONFIG_DATASET_NAME].format(prefix, sample_id, DAY_POST_SACRIFICE, "CT", RAW)

        dsb = self.raw_dataset_builder(base_keywords=self.config[CONFIG_KEYWORDS]).\
            args(self.args).\
            proposal_id(proposal_dict[PROPOSAL_ID_API]).\
            owner(get_ownername(directory)).\
            source_folder(directory).\
            is_published(self.args.publish).\
            size(total_size).\
            principal_investigator(proposal_dict[PI_LASTNAME]).\
            dataset_name(dataset_name).\
            creation_location(self.config[CONFIG_LOCATION]).\
            creation_time(creation_time).\
            scientific_metadata(smb.build()).\
            number_of_files(len(images_in_folder))

        if sample_id is not None:
            dsb.sample_id(sample_id)

        return dsb.build(), images_in_folder


    def ingest_experiment(self):
        failed = {}

        proposal_dict = ProposalBuilder().\
            args(self.args).\
            proposal_id(PROPOSAL_ID).\
            pi_email(NA).\
            pi_lastname(NA).\
            email(NA).\
            abstract(PROPOSAL_ABSTRACT).\
            title(PROPOSAL_TITLE).\
            start_time(PROPOSAL_START).\
            end_time(PROPOSAL_END).\
            build()
        resp = API.proposal_ingest(self.args.token, proposal_dict, self.args.simulation, self.args.verbose)
        if resp.status_code != 200:
            failed[proposal_dict[PROPOSAL_ID_API]] = resp.text

        ct_directory = "{}/{}".format(self.config[CONFIG_SOURCE_PATH], PATH_CT)

        for dataset in sorted(list_dirs(ct_directory)):
            
            dataset_ct_directory = "{}/{}".format(ct_directory, dataset)
            named_dirs = list_dirs(dataset_ct_directory)
            assert len(named_dirs) == 1
            dataset_ct_directory = "{}/{}".format(dataset_ct_directory, named_dirs[0])
    
            # Add raw dataset
            smb = ScientificMetadataBuilder()
            dataset_dict, filename_list = self._create_raw(dataset, dataset_ct_directory, None, smb, proposal_dict, None, self.config[CONFIG_PREFIX], None)
            datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
            attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_dict[PROPOSAL_ID_API])
            failed.update(failed_attachments)
            dataset_dict[SOURCE_FOLDER] = dataset_dict[SOURCE_FOLDER].replace('/home/lucaschr', '~')
            failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))

        if failed:    
            print("\n---!--- FAILURES ---!---")
            for key in sorted(failed.keys()):
                print("\n=>", key, "\n", failed[key], "\n")
        
