from ...Proposals.Proposal import ProposalBuilder
from ...Proposals.APIKeys import PROPOSAL_ID as PROPOSAL_ID_API
from ...Proposals.APIKeys import PI_LASTNAME
from .Consts import *
from ..Beamline.Ingestion import AbstractIngestor
from ..Beamline.ConfigKeys import *
from ..Beamline.Consts import RAW
from ...Datasets.DatasetVirtual import ZTLMRDatasetBuilder
from ...Datasets.APIKeys import SOURCE_FOLDER
from ...Filesystem.FSInfo import list_dirs, list_files, get_creation_date, folder_total_size
from ...Filesystem.FSInfoUnix import get_ownername
from ...Filesystem.ImInfo import load_numpy_from_image
from ...Datasets.Dataset import AttachmentBuilder, ScientificMetadataBuilder
from ...REST.Consts import NA
from ...REST import API


class ZTLMRIngestor(AbstractIngestor):
    def __init__(self, args):
        config = {
            CONFIG_LOG_SUFFIX: LOG_SUFFIX,
            CONFIG_LOG_FILENAMES: LOG_FILENAMES,
            CONFIG_LOCATION: LOCATION,
            CONFIG_KEYWORDS: KEYWORDS,
            CONFIG_SOURCE_PATH: SOURCE_PATH,
            CONFIG_PREFIX: SITE_PREFIX,
            CONFIG_FILENAME_IGNORE: FILENAME_IGNORE_PATTERN,
            CONFIG_DATASET_NAME: DATASET_NAME_PATTERN
        }
        super().__init__(args, config, ZTLMRDatasetBuilder, None, None)
    
    def _parse_dataset(self, dataset):
        date = dataset[17:25]
        pos_day = dataset[26:].find("__") 
        day = dataset[26:26+pos_day]
        if day == 'FINAL':
            day = 'd72'
        pos_seq = dataset[26+pos_day:].find("E") 
        seq = dataset[26+pos_day+pos_seq:26+pos_day+pos_seq+2]  # TurboRare T2 or DWI
        if seq == "E2":
            seq = "turboRare_T2"
        elif seq == "E7":
            seq = "diffusion_DWI"
        return date, day, seq

    def _create_raw(self, dataset, directory, creation_time, smb, proposal_dict, sample_id, prefix, histo_id):
        date, day, seq = self._parse_dataset(dataset)

        dataset_name = self.config[CONFIG_DATASET_NAME].format(prefix, sample_id, day, seq, RAW)

        smb.set_value("Date of Image", date)
        smb.set_value("Day after implant", day)
        smb.set_value("MR Sequence", seq)

        images_in_folder = list_files(directory, self.args.extensions)

        for subdir in list_dirs(directory):
            images_in_folder += ["{}/{}".format(subdir, f) for f in list_files("{}/{}".format(directory, subdir), self.args.extensions)]
        images_in_folder = sorted(images_in_folder)

        meta_info_file = "{}/{}".format(directory, images_in_folder[0])
        creation_time = get_creation_date(meta_info_file)
        _, _, dicom_meta = load_numpy_from_image(meta_info_file)
        for tag in DICOM_TAGS:
            value = dicom_meta.get(tag, NA)
            if isinstance(value, list):
                value = ",".join([str(v) for v in value])
            smb.set_value("DICOM_" + tag, value)

        total_size = folder_total_size(directory)

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
            proposal_id("2017-ZTL").\
            pi_email(NA).\
            pi_lastname(NA).\
            email(NA).\
            abstract("From: Medizinische Hochschule Hannover (MHH), Institut für Versuchstierkunde und Zentrales Tierlaboratorium (ZTL), AG Kleintierbildgebung (Martin Meier); In-vivo experiments monitoring the functional changes of tissue parameters during degradation process; Intercondylar in the knee (femur of rat); Implantation of biodegradable material: 8 animals Mg, 8 animals Mg5Gd, 8 animals PEEK, 8 animals control sham; 7 in-vivo observations: Before implant (BL), 0d after implant, 3d after, 7d after, 14d after, 28d after, 56d after, and 72d after (before sacrifice); MR experiments: Bruker Pharmascan 7T and volume coil in S1 specified Lab conditions").\
            title("MHH-ZTL Rat Femur").\
            start_time("2017-01-01").\
            end_time("2017-12-31").\
            build()
        resp = API.proposal_ingest(self.args.token, proposal_dict, self.args.simulation, self.args.verbose)
        if resp.status_code != 200:
            failed[proposal_dict[PROPOSAL_ID_API]] = resp.text

        mr_directory = "{}/{}".format(self.config[CONFIG_SOURCE_PATH], PATH_MR)

        for dataset in sorted(list_dirs(mr_directory)):
            
            dataset_mr_directory = "{}/{}".format(mr_directory, dataset)
            
            # Add raw dataset
            sample_id = dataset[:5]
            smb = ScientificMetadataBuilder()
            dataset_dict, filename_list = self._create_raw(dataset, dataset_mr_directory, None, smb, proposal_dict, sample_id, self.config[CONFIG_PREFIX], None)
            datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
            attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_dict[PROPOSAL_ID_API])
            failed.update(failed_attachments)
            dataset_dict[SOURCE_FOLDER] = dataset_dict[SOURCE_FOLDER].replace('/home/lucaschr', '~')
            failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))

        if failed:    
            print("\n---!--- FAILURES ---!---")
            for key in sorted(failed.keys()):
                print("\n=>", key, "\n", failed[key], "\n")
        