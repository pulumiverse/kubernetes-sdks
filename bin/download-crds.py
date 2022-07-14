from typing import List
from yaml import safe_load, YAMLError
import requests
import tarfile
import sys
from io import BytesIO

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
        crd_url = crd_url.replace('${VERSION}', version)
        if crd_url.endswith('.tar.gz'):
            response = requests.get(crd_url, stream=True)
            with tarfile.open(fileobj=response.raw, mode="r|gz") as tf:
                for (info, crdfile) in ((m, tf.extractfile(m)) for m in tf):
                    if crdfile is not None:
                        f.write(("# url: %s file: %s\n" % (crd_url, info.name)).encode('utf-8'))
                        f.write(crdfile.read())
                        f.write(b"\n---\n")
        else:
            crd = requests.get(crd_url).content
            f.write(("# url: %s\n" % crd_url).encode('utf-8'))
            f.write(crd)
            f.write(b"---\n")
