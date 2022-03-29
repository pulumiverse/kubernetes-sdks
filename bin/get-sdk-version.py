from yaml import safe_load, YAMLError
import sys

with open("./sdks.yaml", "r") as stream:
    try:
        sdks = safe_load(stream)
    except YAMLError as exc:
        print(f"Error parsing SDK Yaml: {exc}")

details = sdks.get(sys.argv[1])
sdk_version_string = f'{sys.argv[1]}|{details["repository"]}|{sys.argv[2]}'

print(sdk_version_string)
