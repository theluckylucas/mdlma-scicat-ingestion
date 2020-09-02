from ScicatTool.P05.Ingestion import ingest_derived
from ScicatTool.Utils.ArgumentsP05 import P05DerivedExperimentParser
import datetime


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = P05DerivedExperimentParser()
    args = parser.parse_args()
    ingest_derived(args)
    print('END', datetime.datetime.now())