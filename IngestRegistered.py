"""
This is the main file to call for adding stiched histo with registered SRCT experiments.
Run python IngestRegistered.py -h for details about how to call.
"""


from ScicatTool.Sites.BeamlineBeritRegistered.Ingestion import BeamlineRegisteredStichedHistoIngestor
from ScicatTool.Utils.ArgumentsBeamline import RegisteredHistoExperimentIngestionParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = RegisteredHistoExperimentIngestionParser()
    args = parser.parse_args()
    print(args)
    BeamlineRegisteredStichedHistoIngestor(args).ingest_experiment()
    print('END', datetime.datetime.now())
