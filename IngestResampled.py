"""
This is the main file to call for adding resampled experiments.
Run python IngestResampled.py -h for details about how to call.
"""


from ScicatTool.Sites.BeamlineJulianResampled.Ingestion import BeamlineResampledIngestor
from ScicatTool.Utils.ArgumentsBeamline import ResampledExperimentIngestionParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = ResampledExperimentIngestionParser()
    args = parser.parse_args()
    BeamlineResampledIngestor(args).ingest_experiment()
    print('END', datetime.datetime.now())
