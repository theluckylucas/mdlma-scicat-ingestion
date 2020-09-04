"""
This is the main file to call for adding P05 experiments.
Run python IngestP05.py -h for details about how to call.
"""


from ScicatTool.P05.Ingestion import ingest_experiment
from ScicatTool.Utils.ArgumentsP05 import P05ExperimentIngestionParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = P05ExperimentIngestionParser()
    args = parser.parse_args()
    ingest_experiment(args)
    print('END', datetime.datetime.now())
