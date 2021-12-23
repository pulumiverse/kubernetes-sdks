from atoma import parse_atom_bytes
from datetime import datetime, timedelta, timezone
from json import dumps
from requests import get as httpget
from typing import List, Mapping, Optional
from yaml import safe_load, YAMLError
import sys

with open("./sdks.yaml", "r") as stream:
    try:
        sdks: Mapping[str, str] = safe_load(stream)
    except YAMLError as exc:
        print(f"Error parsing SDK Yaml: {exc}")

repository = sdks.get(sys.argv[1])
sdk_version_string = f'{sys.argv[1]}|{repository}|{sys.argv[2]}'

print(sdk_version_string)
