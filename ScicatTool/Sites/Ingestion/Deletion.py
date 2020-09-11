from ...REST import API
from ...Datasets.APIKeys import SOURCE_FOLDER, PID, DATASET_NAME, PROPOSAL_ID
from .Consts import PATH_GPFS_P05
from pprint import pprint


def delete_experiment(args):
    failed = {}
    datasets = API.get_datasets(args.token, args.simulation, args.verbose)
    for dataset in datasets:
        if PATH_GPFS_P05.format(args.year, args.experiment) + '/' in dataset[SOURCE_FOLDER]:
            print("---*---", dataset[DATASET_NAME], "---*---")
            resp = API.dataset_delete(args.token, dataset[PID], dataset[DATASET_NAME], args.simulation, args.verbose)
            if resp.status_code != 200:
                failed[dataset[SOURCE_FOLDER]] = resp.text
            elif args.deleteproposals and PROPOSAL_ID in dataset.keys():
                resp = API.proposal_delete(args.token, dataset[PROPOSAL_ID], args.simulation, args.verbose)
                if resp.status_code != 200:
                    failed[dataset[PROPOSAL_ID]] = resp.text
    if failed:
        print('---!--- API FAILURES ---!---')
        for key, value in failed.items():
            print(key)
            print(value)
