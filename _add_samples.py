"""
This is a script for adding samples
"""

from ScicatTool.Samples.Sample import SampleBuilder, SampleCharacteristicsBuilder
from ScicatTool.Datasets.APIKeys import *
from ScicatTool.REST.Consts import HEADERS
import argparse
import datetime
import requests
import pprint
import json
import csv


URL = "https://scicat-mdlma.desy.de/api/v3/{}?access_token={}"


def add_samples(args):
    header = None
    first = True
    samples = {}
    with open(args.filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            if first:
                header = row
                first = False
            else:
                if row[0] in samples.keys():
                    print("Sample duplicate", row[0])
                    exit(0)
                else:
                    scb = SampleCharacteristicsBuilder()
                    for i in range(1, len(header)):
                        scb.add(header[i], row[i])
                    sb = SampleBuilder(row[0]).\
                        owner_group("hasylab").\
                        characteristics(scb.build()).\
                        description(" ".join(["{}"]*len(args.desc_indices)).format(*[row[i] for i in args.desc_indices]))
                    data = sb.build()

                    if args.simulation:
                        print(row[0], "Simulation only!")
                    else:
                        uri = URL.format("samples", args.token)
                        resp = requests.post(uri, headers=HEADERS, data=json.dumps(data))
                        print("Add Sample", row[0], resp)


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = argparse.ArgumentParser()
    parser.add_argument("token", type=str, help="A valid SciCat token of a logged in user (see Settings)")
    parser.add_argument("filename", type=str, help="CSV file with sample data")
    parser.add_argument("desc_indices", type=int, nargs="+", default=[0], help="CSV column indices of information concatenated for description")
    parser.add_argument("-s", "--simulation", action='store_true', help="Simulates full run, but does NOT(!) call API")
    args = parser.parse_args()
    add_samples(args)
    print('END', datetime.datetime.now())