from .Consts import *
from .XMLMetaParser import HistoMetaParser
from ...REST import API
from ...Datasets.Consts import PID_PREFIX
from ...Datasets.Dataset import ScientificMetadataBuilder
from ...Datasets.APIKeys import KEYWORDS as API_KEYWORDS
from ..P05.Consts import LOCATION as P05_LOCATION
from ..P05.Consts import SITE_PREFIX as P05_SITE_PREFIX
from ..P07.Consts import LOCATION as P07_LOCATION
from ..P07.Consts import SITE_PREFIX as P07_SITE_PREFIX
from ..Beamline.Ingestion import AbstractIngestor
from ..Beamline.ConfigKeys import *
from ..Beamline.Consts import PROCESSED
from ...Datasets.DatasetVirtual import HistoRawDatasetBuilder, HistoRegistedDatasetBuilder
from ...Datasets.APIKeys import SOURCE_FOLDER, TYPE, DATASET_NAME, PID, PROPOSAL_ID
from ...Datasets.Consts import TYPE_DERIVED, TYPE_RAW
from ...REST.Consts import NA
from ...Filesystem.FSInfo import list_files, list_dirs, path_exists, get_creation_date
import csv


class BeamlineRegisteredStichedHistoIngestor(AbstractIngestor):
    def __init__(self, args):
        config = {
            CONFIG_LOG_SUFFIX: LOG_SUFFIX,
            CONFIG_LOG_FILENAMES: [],
            CONFIG_LOCATION: LOCATION,
            CONFIG_KEYWORDS: KEYWORDS,
            CONFIG_SOURCE_PATH: PATH_GPFS,
            CONFIG_PREFIX: SITE_PREFIX,
            CONFIG_FILENAME_IGNORE: FILENAME_IGNORE_PATTERN,
            CONFIG_DATASET_NAME: DATASET_NAME_PATTERN
        }
        super().__init__(args, config, HistoRawDatasetBuilder, HistoRegistedDatasetBuilder, None)


    def find_existing_datasets(self, source_folder):
        result = []
        for dataset in self.datasets:
            if source_folder in dataset[SOURCE_FOLDER] and\
                -1 < abs(len(source_folder) - len(dataset[SOURCE_FOLDER])) < 2 and\
                dataset[TYPE] == TYPE_DERIVED and\
                POSTPROCESSING in dataset[API_KEYWORDS]:
                result.append(dataset)
        return result


    def dataset_derived_name(self, pattern, prefix, experiment_id, dataset, post_processing, subdir, suffix):
        return pattern.format(prefix, experiment_id, dataset, post_processing + '-' + suffix)


    def dataset_raw_name(self, pattern, prefix, experiment_id, dataset, post_processing, histo_id):
        return pattern.format(prefix, histo_id, dataset, post_processing)


    def load_csv_mapping(self):
        header = None
        first = True
        samples = {}
        with open(self.args.csvfile, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                if first:
                    header = row
                    first = False
                else:
                    if row[0] in samples.keys():
                        print("Sample duplicate", row[0])
                        exit(0)
                    else:
                        samples[row[0]] = (row[2], row[3])
        return samples


    def ingest_experiment(self):
        failed = {}
        self.datasets = API.get_datasets(self.args.token, self.args.simulation, self.args.verbose)
        directory = PATH_GPFS.format(self.args.beamline, self.args.year, self.args.experiment)
        mapping = self.load_csv_mapping()
        if path_exists(directory):
            for dataset in list_dirs(directory):
                for sample_id in mapping.keys():
                    if dataset.startswith(sample_id):
                        srct_path, histo_id = mapping[sample_id]
                        print(sample_id, srct_path, histo_id)
                        
                        existing = self.find_existing_datasets(srct_path)
                        print(srct_path, "--> Matching {:d} dataset(s) in Scicat".format(len(existing)))
                        if self.args.matchexisting and len(existing) != 1:
                            failed[srct_path] = "Not matching with a single dataset - omitting!"
                            continue

                        raw_root = "{}/{}/{}".format(directory, HISTO_RAW_DIRECTORY, histo_id)
                        xml_filenames = list_files(raw_root, '.xml')
                        
                        for xml_filename in xml_filenames:
                            if xml_filename.endswith(self.config[CONFIG_LOG_SUFFIX]):
                                path_xml_filename = "{}/{}".format(raw_root, xml_filename)
                                xml_metadata = HistoMetaParser(path_xml_filename).get_dict()
                                smb = ScientificMetadataBuilder()
                                for key, value in xml_metadata.items():
                                    smb.add(key, value)
                                creation_time = get_creation_date(path_xml_filename)
                                break

                        proposal_dict = {PROPOSAL_ID: NA, "lastname": NA}  # To be fetched from Scicat
                        if len(existing) == 1:
                            if existing[0][TYPE] == TYPE_RAW:
                                proposal_dict[PROPOSAL_ID] = existing[0][PROPOSAL_ID]

                        # Add raw
                        dataset_dict, filename_list = self._create_raw(dataset, raw_root, creation_time, smb.build(), proposal_dict, sample_id, SITE_PREFIX_HISTO, histo_id)
                        datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
                        attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_dict[PROPOSAL_ID])
                        failed.update(failed_attachments)
                        failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))

                        # Prepare data for derived
                        experiment_id = srct_path[srct_path.find("data/")+len("data/"):srct_path.find(PROCESSED)-1]
                        dataset_name = srct_path[srct_path.find(PROCESSED+"/")+len(PROCESSED+"/"):srct_path.find(POSTPROCESSING)-1]
                        site_prefix = self.config[CONFIG_PREFIX]
                        input_datasets = [PID_PREFIX + dataset_dict[PID]]  # raw histo as input dataset for registered dataset
                        if len(existing) == 1:
                            input_datasets += [existing[0][PID]]  # existing as input for registered dataset
                            site_prefix = existing[0][DATASET_NAME][:existing[0][DATASET_NAME].find('/')]

                        # Add registered data
                        dataset_dict, filename_list = self._create_derived(dataset_name, directory, dataset, POSTPROCESSING, input_datasets, NA, site_prefix, experiment_id, DATASET_NAME_DERIVED_SUFFIX)
                        dataset_dict[API_KEYWORDS] += KEYWORDS_DERIVED
                        datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
                        attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_dict[PROPOSAL_ID])
                        failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))
                        failed.update(failed_attachments)

        if failed:    
            print("\n---!--- FAILURES ---!---")
            for key in sorted(failed.keys()):
                print("\n=>", key, "\n", failed[key], "\n")
