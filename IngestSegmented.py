"""
This is the main file to call for adding segmented experiments.
Run python IngestSegmented.py -h for details about how to call.
"""


from ScicatTool.Sites.BeamlinePhilippSegmented.Ingestion import BeamlineSegmentedIngestor
from ScicatTool.Utils.ArgumentsBeamline import SegmentedExperimentIngestionParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = SegmentedExperimentIngestionParser()
    args = parser.parse_args()
    print(args)
    BeamlineSegmentedIngestor(args).ingest_experiment()
    print('END', datetime.datetime.now())
