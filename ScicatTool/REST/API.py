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


def dataset_ingest(token, data_dict, simulate=False):
    url = get_url(token, "Datasets")
    data = json.dumps(data_dict)
    pprint(data)
    if not simulate:
        resp = requests.post(url, headers=HEADERS, data=data)
        print("DATASET JSON INGEST:", resp)
    return resp


def dataset_delete(token, dataset_pid, dataset_name, simulate=False):
    url = get_url(token, "Datasets", uid=dataset_pid)
    print(dataset_name)
    if not simulate:
        resp = requests.delete(url, headers=HEADERS)
        print("DELETE", dataset_pid, "(PID):", resp)
    return resp


def get_datasets(token):
    url = get_url(token, "Datasets")
    resp = requests.get(url, headers=HEADERS)
    print("GET DATASETS:", resp)
    return json.loads(resp.text)
