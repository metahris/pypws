import json


def load_data(file_path):
    with open(file_path, 'r') as f:
        dct = json.loads(f.read())
    return dct
