"""
This is the main file to call for deletion of P05 experiments.
Run python DeleteP05.py -h for details about how to call.
"""


from ScicatTool.Sites.P05.Deletion import P05Deleter
from ScicatTool.Utils.ArgumentsBeamline import P05ExperimentDeletionParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = P05ExperimentDeletionParser()
    args = parser.parse_args()
    P05Deleter(args).delete_experiment()
    print('END', datetime.datetime.now())
