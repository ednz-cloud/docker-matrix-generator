import os
import json
import re
from collections import defaultdict
from typing import List, Tuple, Dict

OUTPUT = "version_matrix"


def parse_version(version_str: str) -> Tuple[int, int, int]:
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_str)
    if match:
        return tuple(map(int, match.groups()))
    else:
        raise ValueError("Invalid version format: " + version_str)


def get_latest_versions(versions: List[str]) -> List[Dict[str, any]]:
    latest_major = defaultdict(lambda: (0, 0, 0))
    latest_minor = defaultdict(lambda: (0, 0, 0))

    for version in versions:
        major, minor, patch = parse_version(version)
        if (major, minor, patch) > latest_major[major]:
            latest_major[major] = (major, minor, patch)
        if (major, minor, patch) > latest_minor[(major, minor)]:
            latest_minor[(major, minor)] = (major, minor, patch)

    latest_overall = max(versions)

    version_objects = []
    for version in versions:
        major, minor, patch = parse_version(version)
        is_latest = version == latest_overall
        is_latest_major = (major, minor, patch) == latest_major[major]
        is_latest_minor = (major, minor, patch) == latest_minor[(major, minor)]

        version_obj = {
            "version": version,
            "is_latest": is_latest,
            "is_latest_major": is_latest_major,
            "is_latest_minor": is_latest_minor,
        }
        version_objects.append(version_obj)

    return version_objects


def main():
    all_versions_str = os.environ.get("VERSION_LIST", "")
    all_versions = json.loads(all_versions_str)

    version_objects = get_latest_versions(all_versions)

    value = json.dumps(version_objects)

    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        print(f"{OUTPUT}='{value}'", file=fh)


if __name__ == "__main__":
    main()
