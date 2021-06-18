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
URL = "https://scicat-mdlma.desy.de/api/v3/{}/findOne?filter={\"where\":{\"createdBy\": \"ldap.christianlucas\"}}?access_token={}"


def delete_models(args):
    resp = requests.get(URL.format(args.model, args.token), headers=HEADERS, data={})
    if resp.status_code == 200:
        data = json.loads(resp.text)
        print("Found", len(data), "models.")
    else:
        print("Error:", resp.text)
        return
    for dic in data:
        aid = dic[args.idkey].replace("/", "%2F")
        if "TemporalStorage" in dic[args.namekey]:
            if args.simulation:
                print(aid, "- Simulation only! No deletion of", dic[args.namekey])
            else:
                deleted = requests.delete(URL.format(args.model + "/" + aid, args.token), headers=HEADERS)
                if deleted.status_code == 200:
                    print(aid, deleted)
                else:
                    print("Error:", deleted.text)


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
