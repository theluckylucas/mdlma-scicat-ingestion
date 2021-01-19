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
from ...Datasets.DatasetVirtual import SegmentedDatasetBuilder
from ...Datasets.APIKeys import SOURCE_FOLDER, TYPE, DATASET_NAME, PID, PROPOSAL_ID
from ...Datasets.Consts import TYPE_DERIVED, TYPE_RAW
from ...REST.Consts import NA
from ...Filesystem.FSInfo import list_files, list_dirs, path_exists, get_creation_date
import csv


class BeamlineSegmentedIngestor(AbstractIngestor):
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
        super().__init__(args, config, None, SegmentedDatasetBuilder, None)


    def find_existing_datasets_by_directory(self, source_folder, dataset_type):
        result = []
        for dataset in self.datasets:
            if source_folder in dataset[SOURCE_FOLDER] and\
                dataset[TYPE] == dataset_type:
                result.append(dataset)
        return result


    def find_existing_datasets_by_experiment(self, experiment, dataset_name, dataset_type):
        result = []
        for dataset in self.datasets:
            if experiment in dataset[SOURCE_FOLDER] and\
                dataset_name in dataset[SOURCE_FOLDER] and\
                dataset[TYPE] == dataset_type:
                result.append(dataset)
        return result


    def load_csv(self):
        result = {}
        with open(self.args.csvfile, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                if path_exists(row[1]):
                    result[row[0]] = row[1]
        return result

    def get_dataset_name_from_source_folder(self, directory, csv_name, keyword='/processed/'):
        if 'external' in directory:
            pos_2d = csv_name.find('_2D_')
            return csv_name[:pos_2d]
        pos_dataset = directory.find(keyword) + len(keyword)
        len_dataset = directory[pos_dataset:].find('/')
        return directory[pos_dataset:pos_dataset+len_dataset]

    def get_site_and_experiment(self, source_folder):
        if 'external' in source_folder:
            site = 'EXTERNAL'
            pos_id = source_folder.find("5000")
            experiment = source_folder[pos_id : pos_id + 8]
        else:
            START = '/asap3/petra3/gpfs/'
            end_pos = source_folder[len(START):].find('/')
            site = source_folder[len(START):len(START)+end_pos]
            pos_id = source_folder.find("1100")
            experiment = source_folder[pos_id : pos_id + 8]
        return site.upper(), experiment

    def dataset_derived_name(self, pattern, prefix, experiment_id, dataset_name, post_processing, subdir, suffix=None):
        if suffix is None:
            suffix = ""
        return pattern.format(prefix, experiment_id, dataset_name, post_processing + '-' + subdir + suffix)

    def ingest_experiment(self):
        failed = {}
        self.datasets = API.get_datasets(self.args.token, self.args.simulation, self.args.verbose)
        print("Total number of datasets in Scicat:", len(self.datasets))
        segmented = self.load_csv()
        for csv_name, csv_directory in segmented.items():
            print("\n" + csv_name)

            dataset_from_csv = self.get_dataset_name_from_source_folder(csv_directory, csv_name)

            if csv_name.endswith(IMAGES_FULL):  # original data

                existing_directory = self.find_existing_datasets_by_directory(csv_directory, TYPE_DERIVED)
                print(csv_name, "--> Matching {:d} existing dataset(s) in Scicat by source folder".format(len(existing_directory)))

                dataset_dict = None
                proposal_id = NA
                input_datasets = [NA]

                # 1. add original data, if not yet in scicat
                if len(existing_directory) > 1:
                    failed[csv_name] = "More than one dataset exists with identical source folder - skipping!"
                    continue
                elif len(existing_directory) == 1:
                    dataset_dict = existing_directory[0]
                    
                    print("existing dataset:", dataset_dict[PID])
                    input_datasets = [dataset_dict[PID]]
                else:
                    site_prefix, experiment_id = self.get_site_and_experiment(csv_directory)
                    print("SITE", site_prefix, " | EXPERIMENT", experiment_id)

                    existing_raw_dataset = self.find_existing_datasets_by_experiment(experiment_id, dataset_from_csv, TYPE_RAW)
                    print(dataset_from_csv, "--> {:d} possible raw dataset(s) in Scicat found".format(len(existing_raw_dataset)))
                    if self.args.matchexisting and len(existing) != 1:
                        failed[dataset_name] = "Not matching with a single existing dataset - skipping!"
                        continue
                    
                    if len(existing_raw_dataset) == 1:
                        input_datasets = [existing_raw_dataset[0][PID]]
                        if PROPOSAL_ID in existing_raw_dataset[0].keys():
                            proposal_id = existing_raw_dataset[0][PROPOSAL_ID]                    

                    dataset_dict, filename_list = self._create_derived(dataset_from_csv, csv_directory, "", POSTPROCESSING, input_datasets, NA, site_prefix, experiment_id, IMAGES_FULL)
                    datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
                    attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_id)
                    failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))
                    failed.update(failed_attachments)

                    print("new dataset:", dataset_dict[PID])
                    input_datasets = ["{}{}".format(PID_PREFIX, dataset_dict[PID])]

                dataset_dict = None
                if not len(input_datasets) == 1 or not NA in input_datasets:

                    # 2. add processed image data, if not yet in scicat
                    csv_name_processed = csv_name[:-len(IMAGES_FULL)] + IMAGES
                    csv_directory_processed = segmented[csv_name_processed]
                    dataset_from_csv_processed = self.get_dataset_name_from_source_folder(csv_directory_processed, csv_name_processed)

                    existing_directory = self.find_existing_datasets_by_directory(csv_directory_processed, TYPE_DERIVED)
                    print(csv_name_processed, "--> Matching {:d} existing processed dataset(s) in Scicat by source folder".format(len(existing_directory)))

                    if len(existing_directory) > 1:
                        failed[csv_name] = "More than one dataset exists with identical source folder - skipping!"
                        continue
                    elif len(existing_directory) == 1:
                        dataset_dict = existing_directory[0]
                        
                        print("existing dataset:", dataset_dict[PID])
                        input_datasets = [dataset_dict[PID]]
                    else:
                        dataset_dict, filename_list = self._create_derived(dataset_from_csv_processed,
                                                                            csv_directory_processed,
                                                                            "",
                                                                            POSTPROCESSING,
                                                                            input_datasets,
                                                                            NA,
                                                                            site_prefix,
                                                                            experiment_id,
                                                                            IMAGES)
                        datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
                        attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_id)
                        failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))
                        failed.update(failed_attachments)

                        print("new dataset:", dataset_dict[PID])
                        input_datasets = ["{}{}".format(PID_PREFIX, dataset_dict[PID])]

                    dataset_dict = None
                    if not len(input_datasets) == 1 or not NA in input_datasets:

                        # 3. add label data, if not yet in scicat
                        csv_name_label = csv_name[:-len(IMAGES_FULL)] + LABELS
                        csv_directory_label = segmented[csv_name_label]
                        dataset_from_csv_label = self.get_dataset_name_from_source_folder(csv_directory_label, csv_name_label)

                        existing_directory = self.find_existing_datasets_by_directory(csv_directory_label, TYPE_DERIVED)
                        print(csv_name_label, "--> Matching {:d} existing label dataset(s) in Scicat by source folder".format(len(existing_directory)))

                        if not existing_directory:
                            dataset_dict, filename_list = self._create_derived(dataset_from_csv_label,
                                                                                csv_directory_label,
                                                                                "",
                                                                                POSTPROCESSING,
                                                                                input_datasets,
                                                                                NA,
                                                                                site_prefix,
                                                                                experiment_id,
                                                                                LABELS)
                            datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
                            attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_id)
                            failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))
                            failed.update(failed_attachments)

                            print("new dataset:", dataset_dict[PID])

                                # TODO kezwords!!!!
            

            """
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
                                smb.set_value(key, value)
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
                    dataset_dict, filename_list = self._create_derived(dataset_name, directory, dataset, POSTPROCESSING, input_datasets, None, site_prefix, experiment_id, DATASET_NAME_DERIVED_SUFFIX)
                    dataset_dict[API_KEYWORDS] += KEYWORDS_DERIVED
                    datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
                    attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, proposal_dict[PROPOSAL_ID])
                    failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))
                    failed.update(failed_attachments)
            """
        if failed:    
            print("\n---!--- FAILURES ---!---")
            for key in sorted(failed.keys()):
                print("\n=>", key, "\n", failed[key], "\n")
