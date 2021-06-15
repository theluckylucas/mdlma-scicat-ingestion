"""
This is the main file to call for adding MR and CT data from ZTL.
Run python IngestZTL.py -h for details about how to call.
"""


from ScicatTool.Sites.ZTL.Ingestion_MR import ZTLMRIngestor
from ScicatTool.Utils.ArgumentsFilesystem import ZTLIngestionParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser =ZTLIngestionParser()
    args = parser.parse_args()
    print(args)
    ZTLMRIngestor(args).ingest_experiment()
    print('END', datetime.datetime.now())
