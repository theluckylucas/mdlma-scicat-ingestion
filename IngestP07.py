"""
This is the main file to call for adding P07 experiments.
Run python IngestP07.py -h for details about how to call.
"""


from ScicatTool.Sites.P07.Ingestion import P07Ingestor
from ScicatTool.Utils.ArgumentsBeamline import P07ExperimentIngestionParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = P07ExperimentIngestionParser()
    args = parser.parse_args()
    P07Ingestor(args).ingest_experiment()
    print('END', datetime.datetime.now())
