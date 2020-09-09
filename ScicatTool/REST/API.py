from pprint import pprint
import requests
import json
import time

from .Consts import *


def get_url(token, entity, model_id=None, member=None, func=None):
    if model_id is None:
        model_id = ""
    else:
        model_id = '/' + model_id.replace('/','%2F')
    if member is None:
        member = ""
    else:
        member = '/' + member.replace('/','%2F')
    if func is None:
        func = ""
    else:
        func = '/' + func.replace('/','%2F')
    return URL_PATTERN.format(SERVER_PROTOCOL, SERVER_URL, SERVER_API_VERSION, entity, model_id, member, func, token)


def ingest(token, data_model, data_dict, simulate, verbose):
    assert data_model in DATA_MODELS
    url = get_url(token, data_model)
    data = json.dumps(data_dict)
    if verbose:
        print(url)
        pprint(data)
    if not simulate:
        resp = requests.post(url, headers=HEADERS, data=data)
        print(data_model.upper(), "JSON INGEST:", resp)
        return resp
    return requests.Response()


def proposal_ingest(token, data_dict, simulate=False, verbose=False):
    return ingest(token, PROPOSALS, data_dict, simulate, verbose)


def dataset_ingest(token, data_dict, simulate=False, verbose=False):
    return ingest(token, DATASETS, data_dict, simulate, verbose)


def origdatablock_ingest(token, data_dict, simulate=False, verbose=False):
    if verbose == 1:
        return ingest(token, ORIGDATABLOCKS, data_dict, simulate, False)
    return ingest(token, ORIGDATABLOCKS, data_dict, simulate, verbose)


def dataset_attach(token, data_dict, model_id, simulate=False, verbose=False):
    url = get_url(token, DATASETS, model_id=model_id, member=ATTACHMENTS)
    data = json.dumps(data_dict)
    if verbose > 1:
        print(url)
        pprint(data)
    if not simulate:
        resp = requests.post(url, headers=HEADERS, data=data)
        print(DATASETS, "JSON ATTACH:", resp)
        return resp
    return requests.Response()


def delete(token, data_model, model_id, simulate, verbose):
    assert data_model in DATA_MODELS
    url = get_url(token, data_model, model_id=model_id)
    if verbose:
        print(url)
    if not simulate:
        resp = requests.delete(url, headers=HEADERS)
        print("DELETE", model_id, "(PID):", resp)
        return resp
    return requests.Response()


def dataset_delete(token, dataset_pid, dataset_name, simulate=False, verbose=False):
    print(dataset_name)
    return delete(token, DATASETS, dataset_pid, simulate, verbose)


def proposal_delete(token, proposal_id, simulate=False, verbose=False):
    print(proposal_id)
    return delete(token, PROPOSALS, proposal_id, simulate, verbose)


def get_datasets(token, simulate=False, verbose=False):
    url = get_url(token, "Datasets")
    if verbose:
        print(url)
    if not simulate:
        resp = requests.get(url, headers=HEADERS)
        print("GET DATASETS:", resp)
        return json.loads(resp.text)
    return []
