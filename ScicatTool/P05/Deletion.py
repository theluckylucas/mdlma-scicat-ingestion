from ..REST import API
from ..Datasets.Keys import SOURCE_FOLDER, PID, DATASET_NAME
from ..P05.Consts import PATH_GPFS_P05
from pprint import pprint


def delete_experiment(args):
    failed = []
    datasets = API.get_datasets(args.token)
    for dataset in datasets:
        if PATH_GPFS_P05.format(args.year, args.experiment) + '/' in dataset[SOURCE_FOLDER]:
            resp = API.dataset_delete(args.token, dataset[PID], dataset[DATASET_NAME], args.simulation)
            if resp.status_code != 200:
                failed[dataset_dict[SOURCE_FOLDER]] = resp.text
    print('-!- FAILURES -!-')
    for key, value in failed.items():
        print(key)
        print(value)