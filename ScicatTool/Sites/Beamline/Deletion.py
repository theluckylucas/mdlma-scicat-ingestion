from abc import ABC

from ...REST import API
from .Keys import *


class AbstractDeleter(ABC):
    def __init__(self, args, config):
        super().__init__()
        self.args = args
        self.config = config

    def delete_experiment(self):
        failed = {}
        datasets = API.get_datasets(self.args.token, self.args.simulation, self.args.verbose)
        for dataset in datasets:
            if self.config[CONFIG_SOURCE_PATH].format(self.args.year, self.args.experiment) + '/' in dataset[SOURCE_FOLDER]:
                print("---*---", dataset[DATASET_NAME], "---*---")
                resp = API.dataset_delete(self.args.token, dataset[PID], dataset[DATASET_NAME], self.args.simulation, self.args.verbose)
                if resp.status_code != 200:
                    failed[dataset[SOURCE_FOLDER]] = resp.text
                elif self.args.deleteproposals and PROPOSAL_ID in dataset.keys():
                    resp = API.proposal_delete(self.args.token, dataset[PROPOSAL_ID], self.args.simulation, self.args.verbose)
                    if resp.status_code != 200:
                        failed[dataset[PROPOSAL_ID]] = resp.text
        if failed:
            print("\n---!--- FAILURES ---!---")
            for key, value in failed.items():
                print(key)
                print(value)
