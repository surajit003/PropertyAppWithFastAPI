import json

from settings import TEST_DATA_DIR


def read_json(filename):
    with open(TEST_DATA_DIR.joinpath(filename)) as resp_file:
        return json.load(resp_file)
