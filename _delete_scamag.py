"""
This is a script for deleting all instances of a model
"""

import requests
import json
import argparse
import datetime
from pprint import pprint



HEADERS = {
    'Content-Type': 'application/json',
    'Accept':       'application/json'
}
URL = "https://scicat-mdlma.desy.de/api/v3/{}{}?access_token={}"


def delete_models(args):
    resp = requests.get(URL.format(args.model, "", args.token), headers=HEADERS, data={})
    if resp.status_code == 200:
        data = json.loads(resp.text)
    else:
        print("Error:", resp.text)
        return
    for dic in data:
        aid = dic[args.idkey].replace("/", "%2F")
        if "MHH-SCAMAG" in dic[args.namekey]:

            respd = requests.get(URL.format(args.model, "/" + aid + "/attachments", args.token), headers=HEADERS, data={})
            if resp.status_code == 200:
                ddata = json.loads(respd.text)
            else:
                print("Error:", respd.text)
                return
            for att in ddata:
                if args.simulation:
                    print(aid, dic[args.namekey], "- Simulation only! No deletion of Attachment", att['id'])
                else:
                    deleted = requests.delete(URL.format("attachments", "/" + att['id'], args.token), headers=HEADERS)
                    if deleted.status_code == 200:
                        print(att['id'], deleted)
                    else:
                        print("Error:", deleted.text)
                        return

            respd = requests.get(URL.format(args.model, "/" + aid + "/origdatablocks", args.token), headers=HEADERS, data={})
            if resp.status_code == 200:
                ddata = json.loads(respd.text)
            else:
                print("Error:", respd.text)
                return
            for odb in ddata:
                if args.simulation:
                    print(aid, dic[args.namekey], "- Simulation only! No deletion of Datablock", odb['id'])
                else:
                    print(odb)  #['id'])
                    deleted = requests.delete(URL.format("origdatablocks", "/" + odb['id'], args.token), headers=HEADERS)
                    if deleted.status_code == 200:
                        print(odb['id'], deleted)
                    else:
                        print("Error:", deleted.text)
                        return


            deleted = requests.delete(URL.format(args.model, "/" + aid, args.token), headers=HEADERS)
            if resp.status_code == 200:
                print(aid, deleted)
            else:
                print("Error:", deleted.text)
                return


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = argparse.ArgumentParser()
    parser.add_argument("token", type=str, help="A valid SciCat token of a logged in user (see Settings)")
    parser.add_argument("model", type=str, help="Scicat model, e.g. 'datasets'")
    parser.add_argument("idkey", type=str, default="id", help="Key for model ID, e.g. 'pid'")
    parser.add_argument("namekey", type=str, default="title", help="Key for model name, e.g. 'title'")
    parser.add_argument("-s", "--simulation", action='store_true', help="Simulates full run, but does NOT(!) call API")
    args = parser.parse_args()
    delete_models(args)
    print('END', datetime.datetime.now())
