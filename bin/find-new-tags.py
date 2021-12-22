from atoma import parse_atom_bytes
from datetime import datetime, timedelta, timezone
from json import dumps
from requests import get as httpget
from typing import List, Optional, TypedDict
from yaml import safe_load, YAMLError
import sys


class Sdk(TypedDict):
    name: str
    repository: int
    directory: str


def has_been_updated(updated_at: Optional[datetime] = None) -> bool:
    if updated_at == None:
        return False
    hours_since: int = int(sys.argv[1]) if len(sys.argv) > 1 else 12

    return (datetime.now(timezone.utc) - updated_at) < timedelta(hours=hours_since)


def get_new_tags(sdk: Sdk) -> List[str]:
    response = httpget(f'{sdk["repository"]}/tags.atom')
    feed = parse_atom_bytes(response.content)

    return list(map(lambda entry: entry.title.value, filter(lambda entry: has_been_updated(entry.updated), feed.entries)))


with open("./sdks.yaml", "r") as stream:
    try:
        # This doesn't actually enforce our schema,
        # but I've decided to keep it in for now
        # and will maybe drop in typeguard in the future
        sdks: List[Sdk] = safe_load(stream)
    except YAMLError as exc:
        print(f"Error parsing SDK Yaml: {exc}")


sdks_to_build: List[str] = []
for sdk in sdks:
    for tag in get_new_tags(sdk):
        sdks_to_build.append(
            f'{sdk["name"]}|{sdk["repository"]}|{sdk["directory"]}|{tag}')

print(dumps(sdks_to_build))
