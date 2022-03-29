from typing import List
from yaml import safe_load, YAMLError
import requests
import sys

with open("./sdks.yaml", "r") as stream:
    try:
        sdks = safe_load(stream)
    except YAMLError as exc:
        print(f"Error parsing SDK Yaml: {exc}")

version: str = sys.argv[2]
details = sdks.get(sys.argv[1])
crd_urls: List[str] = details["crds"]

with open("crd.yaml", 'wb') as f:
    for crd_url in crd_urls:
        crd = requests.get(crd_url.replace('${VERSION}', version)).content
        f.write(crd)
        f.write(b"---\n")
