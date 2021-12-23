from atoma import parse_atom_bytes
from datetime import datetime, timedelta, timezone
from json import dumps
from requests import get as httpget
from typing import List, Mapping, Optional
from yaml import safe_load, YAMLError
import sys


def has_been_updated(updated_at: Optional[datetime] = None) -> bool:
    if updated_at == None:
        return False
    hours_since: int = int(sys.argv[1]) if len(sys.argv) > 1 else 12

    return (datetime.now(timezone.utc) - updated_at) < timedelta(hours=hours_since)


def get_new_tags(repository: str) -> List[str]:
    response = httpget(f'https://{repository}/tags.atom')
    feed = parse_atom_bytes(response.content)

    return list(map(lambda entry: entry.title.value, filter(lambda entry: has_been_updated(entry.updated), feed.entries)))


with open("./sdks.yaml", "r") as stream:
    try:
        sdks: Mapping[str, str] = safe_load(stream)
    except YAMLError as exc:
        print(f"Error parsing SDK Yaml: {exc}")

sdks_to_build: List[str] = []
for name, repository in sdks.items():
    for tag in get_new_tags(repository):
        sdks_to_build.append(
            f'{name}|{repository}|{tag}')

print(dumps(sdks_to_build))
