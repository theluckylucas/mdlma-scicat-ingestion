from ScicatTool.P05.Ingestion import ingest
from ScicatTool.Utils.ArgumentsP05 import P05DerivedExperimentParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = P05DerivedExperimentParser()
    args = parser.parse_args()
    ingest(args)
    print('END', datetime.datetime.now())