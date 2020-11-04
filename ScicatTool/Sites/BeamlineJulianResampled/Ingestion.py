from .Consts import *
from ...REST import API
from ...Datasets.APIKeys import KEYWORDS as API_KEYWORDS
from ..P05.Consts import LOCATION as P05_LOCATION
from ..P05.Consts import SITE_PREFIX as P05_SITE_PREFIX
from ..P07.Consts import LOCATION as P07_LOCATION
from ..P07.Consts import SITE_PREFIX as P07_SITE_PREFIX
from ..Beamline.Ingestion import AbstractIngestor
from ..Beamline.ConfigKeys import *
from ...Datasets.DatasetVirtual import VirtualDatasetBuilder
from ...Datasets.APIKeys import SOURCE_FOLDER, TYPE, DATASET_NAME, PID, PROPOSAL_ID
from ...Datasets.Consts import TYPE_DERIVED
from ...REST.Consts import NA
from ...Filesystem.FSInfo import list_files, list_dirs, path_exists


class BeamlineResampledIngestor(AbstractIngestor):
    def __init__(self, args):
        config = {
            CONFIG_LOG_SUFFIX: "",
            CONFIG_LOG_FILENAMES: [],
            CONFIG_LOCATION: LOCATION,
            CONFIG_KEYWORDS: ["resampled"],
            CONFIG_SOURCE_PATH: PATH_GPFS,
            CONFIG_PREFIX: SITE_PREFIX,
            CONFIG_FILENAME_IGNORE: FILENAME_IGNORE_PATTERN,
            CONFIG_DATASET_NAME: DATASET_NAME_PATTERN
        }
        super().__init__(args, config, None, VirtualDatasetBuilder, None)


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
        return pattern.format(prefix, experiment_id, dataset, post_processing)


    def ingest_experiment(self):
        failed = {}
        self.datasets = API.get_datasets(self.args.token, self.args.simulation, self.args.verbose)
        directory = PATH_GPFS.format(self.args.beamline, self.args.year, self.args.experiment)
        if path_exists(directory):
            for dataset in list_dirs(directory):
                pos_id = dataset.find("_1100")
                experiment_id = dataset[pos_id + 1: pos_id + 9]
                dataset_name = dataset[pos_id + 10:]
                existing = self.find_existing_datasets(experiment_id, dataset_name)
                
                print(dataset_name, "--> Matching {:d} raw dataset(s) in Scicat".format(len(existing)))
                if self.args.matchexisting and len(existing) != 1:
                    failed[dataset_name] = "Not matching with a single existing dataset - omitting!"
                    continue
                
                site_prefix = self.config[CONFIG_PREFIX]
                if len(existing) == 1:
                    input_datasets = [existing[0][PID]]  # dataset as input for derived dataset
                    
                    location = existing[0][CREATION_LOCATION]
                    if location == P05_LOCATION:
                        site_prefix = P05_SITE_PREFIX
                    elif location == P07_LOCATION:
                        site_prefix = P07_SITE_PREFIX
                else:
                    input_datasets = [NA]

                dataset_dict, filename_list = self._create_derived(dataset_name, directory, dataset, POSTPROCESSING, input_datasets, NA, site_prefix, experiment_id)
                datablock_dict = self._create_origdatablock(filename_list, dataset_dict)
                attachment_dicts, failed_attachments = self._create_attachments(filename_list, dataset_dict, existing_raw[0][PROPOSAL_ID])
                failed.update(self._api_dataset_ingest(dataset_dict, datablock_dict, attachment_dicts))
                failed.update(failed_attachments)

        if failed:    
            print("\n---!--- FAILURES ---!---")
            for key in sorted(failed.keys()):
                print("\n=>", key, "\n", failed[key], "\n")
