"""
This is the main file to call for deletion of P07 experiments.
Run python DeleteP07.py -h for details about how to call.
"""


from ScicatTool.Sites.P07.Deletion import P07Deleter
from ScicatTool.Utils.ArgumentsBeamline import P07ExperimentDeletionParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = P07ExperimentDeletionParser()
    args = parser.parse_args()
    print(args)
    P07Deleter(args).delete_experiment()
    print('END', datetime.datetime.now())
