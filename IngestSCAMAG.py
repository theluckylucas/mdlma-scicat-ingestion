"""
This is the main file to call for adding MR and CT data from ZTL.
Run python IngestZTL.py -h for details about how to call.
"""


from ScicatTool.Sites.SCAMAG.Ingestion import SCAMAGIngestor
from ScicatTool.Utils.ArgumentsFilesystem import SCAMAGIngestionParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = SCAMAGIngestionParser()
    args = parser.parse_args()
    print(args)
    SCAMAGIngestor(args).ingest_experiment()
    print('END', datetime.datetime.now())
