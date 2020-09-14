"""
This is the main file to call for adding P05 experiments.
Run python IngestP05.py -h for details about how to call.
"""


from ScicatTool.Sites.P05.Ingestion import P05Ingestor
from ScicatTool.Utils.ArgumentsBeamline import P05ExperimentIngestionParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = P05ExperimentIngestionParser()
    args = parser.parse_args()
    P05Ingestor(args).ingest_experiment()
    print('END', datetime.datetime.now())
