from ScicatTool.P05.Ingestion import ingest_experiment
from ScicatTool.Utils.ArgumentsP05 import P05ExperimentParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = P05ExperimentParser()
    args = parser.parse_args()
    ingest_experiment(args)
    print('END', datetime.datetime.now())