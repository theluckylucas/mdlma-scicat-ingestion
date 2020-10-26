from abc import ABC

from ...REST import API
from .ConfigKeys import *
from ...Datasets.APIKeys import SOURCE_FOLDER, DATASET_NAME, PID, PROPOSAL_ID, ATTACHMENT_ID
from ...Datablocks.APIKeys import ID as ODB_ID


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

                if self.args.datablocks:
                    datablocks = API.get_dataset_origdatablocks(self.args.token, dataset[PID], self.args.simulation, self.args.verbose)
                    for datablock in datablocks:
                        resp = API.origdatablock_delete(self.args.token, datablock[ODB_ID], self.args.simulation, self.args.verbose)
                        if resp.status_code != 200:
                            failed[datablock[ODB_ID]] = resp.text

                if self.args.attachments:
                    attachments = API.get_dataset_attachments(self.args.token, dataset[PID], self.args.simulation, self.args.verbose)
                    for attachment in attachments:
                        resp = API.attachment_delete(self.args.token, attachment[ATTACHMENT_ID], self.args.simulation, self.args.verbose)
                        if resp.status_code != 200:
                            failed[attachment[ATTACHMENT_ID]] = resp.text

                resp = API.dataset_delete(self.args.token, dataset[PID], dataset[DATASET_NAME], self.args.simulation, self.args.verbose)

                if resp.status_code != 200:
                    failed[dataset[SOURCE_FOLDER]] = resp.text
                elif self.args.proposals and PROPOSAL_ID in dataset.keys():
                    resp = API.proposal_delete(self.args.token, dataset[PROPOSAL_ID], self.args.simulation, self.args.verbose)
                    if resp.status_code != 200:
                        failed[dataset[PROPOSAL_ID]] = resp.text
        if failed:
            print("\n---!--- FAILURES ---!---")
            for key, value in failed.items():
                print(key)
                print(value)
