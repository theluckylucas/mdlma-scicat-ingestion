"""
This is a script for adding samples
"""

from ScicatTool.Samples.Sample import SampleBuilder, SampleCharacteristicsBuilder
from ScicatTool.Datasets.APIKeys import *
from ScicatTool.REST.Consts import HEADERS
import requests
import pprint
import json
import csv


tkn = "ZWFfE3jboODyFSr6WcJKHQGAhwvBMnEkPsUzwMay8XNLogmvHpJpAw6CUdLd5j4f"
url = "https://scicat-mdlma.desy.de/api/v3/{}?access_token={}"


header = None
first = True
samples = {}
with open('_samples_synchroload.csv', newline='') as csvfile:
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
                    description("{} {} {}".format(row[0], row[7], row[6]))
                data = json.dumps(sb.build())

                #pprint.pprint(data)
                uri = url.format("samples", tkn)
                resp = requests.post(uri, headers=HEADERS, data=data)
                print("\n Add Sample ", uri, "=>", resp, resp.text)