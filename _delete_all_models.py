"""
This is a script for deleting all instances of a model
"""

import requests
import json


model = "attachments"
token = "dStUEq2Or7SQ1YXbPaEut2O4JTujroSxs1bYid7N5rOvWsL3nD55hbcfESCHN8Fh"


HEADERS = {
    'Content-Type': 'application/json',
    'Accept':       'application/json'
}
URL = "https://scicat-mdlma.desy.de/api/v3/{}/{}?access_token={}"
ID = "id"


if __name__ == '__main__':
    resp = requests.get(URL.format(model, "findOne", token), headers=HEADERS, data={})
    while resp.status_code == 200:
        dic = json.loads(resp.text)
        aid = dic[ID]
        print(aid, requests.delete(URL.format(model, aid, token), headers=HEADERS, data={}))
        resp = requests.get(URL.format(model, "findOne", token), headers=HEADERS, data={})

