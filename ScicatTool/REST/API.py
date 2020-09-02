from pprint import pprint
import requests
import json
import time


URL_PATTERN = "{}://{}/api/v{}/{}{}{}{}?access_token={}"
SERVER_PROTOCOL = "http"
SERVER_URL = "scicat-mdlma.desy.de"
SERVER_API_VERSION = 3
HEADERS = {
    'Content-Type': 'application/json',
    'Accept':       'application/json'
}


def get_url(token, entity, uid=None, member=None, func=None):
    if uid is None:
        uid = ""
    else:
        uid = '/' + uid.replace('/','%2F')
    if member is None:
        member = ""
    else:
        member = '/' + member.replace('/','%2F')
    if func is None:
        func = ""
    else:
        func = '/' + func.replace('/','%2F')
    return URL_PATTERN.format(SERVER_PROTOCOL, SERVER_URL, SERVER_API_VERSION, entity, uid, member, func, token)


def dataset_ingest(token, data_dict):
    url = get_url(token, "Datasets")
    pprint(data_dict)
    resp = requests.post(url, headers=HEADERS, data=json.dumps(data_dict))
    print("DATASET INGEST:", resp)
    

def dataset_update(token, dataset_id, data_dict):
    url = get_url(token, "Datasets", uid=dataset_id)
    resp = requests.patch(url, headers=HEADERS, data=json.dumps(data_dict))
    print("DATASET UPDATE:", resp)