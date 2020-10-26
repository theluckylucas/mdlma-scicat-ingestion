"""
This is a script for deleting all instances of a model
"""

import requests
import json
import argparse
import datetime



HEADERS = {
    'Content-Type': 'application/json',
    'Accept':       'application/json'
}
URL = "https://scicat-mdlma.desy.de/api/v3/{}/{}?access_token={}"


def delete_models(args):
    resp = requests.get(URL.format(args.model, "findOne", args.token), headers=HEADERS, data={})
    while resp.status_code == 200:
        dic = json.loads(resp.text)
        aid = dic[args.idkey]
        print(aid, requests.delete(URL.format(args.model, aid, args.token), headers=HEADERS, data={}))
        resp = requests.get(URL.format(args.model, "findOne", args.token), headers=HEADERS, data={})


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = argparse.ArgumentParser()
    parser.add_argument("token", type=str, help="A valid SciCat token of a logged in user (see Settings)")
    parser.add_argument("model", type=str, help="Scicat model, e.g. 'datasets'")
    parser.add_argument("idkey", type=str, default="id", help="Key for model ID, e.g. 'pid'")
    args = parser.parse_args()
    delete_models(args)
    print('END', datetime.datetime.now())