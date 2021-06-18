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
URL = "https://scicat-mdlma.desy.de/api/v3/{}?access_token={}"

list_ids = ["PP2019-SCAMAG"]

def delete_models(args):
    for aid in list_ids:
        aid = aid.replace("/", "%2F")
        if args.simulation:
            print(aid, "- Simulation only! No deletion")
        else:
            print(URL.format("proposals/" + aid, args.token))
            deleted = requests.delete(URL.format("proposals/" + aid, args.token), headers=HEADERS)
            if deleted.status_code == 200:
                print(aid, deleted)
            else:
                print("Error:", deleted.text)


if __name__ == '__main__':
    print('START', datetime.datetime.now())
    parser = argparse.ArgumentParser()
    parser.add_argument("token", type=str, help="A valid SciCat token of a logged in user (see Settings)")
    parser.add_argument("-s", "--simulation", action='store_true', help="Simulates full run, but does NOT(!) call API")
    args = parser.parse_args()
    delete_models(args)
    print('END', datetime.datetime.now())
