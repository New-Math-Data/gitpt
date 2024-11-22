import logging
import os

import tomli

log = logging.getLogger(__name__)


def get_toml_path(toml_data, path):
    # Split path into parts and handle empty path
    if not path:
        return toml_data
    path_parts = path.split(".", 1)

    log.debug("splitting path")
    log.debug(path_parts)

    # Base case - return value if single path part
    if len(path_parts) == 1:
        return toml_data.get(path_parts[0])

    # Recursive case - get first part and recurse on remainder
    first = path_parts[0]
    remainder = path_parts[1]

    # Return None if key not found
    if first not in toml_data:
        return None

    return get_toml_path(toml_data[first], remainder)


def read_toml_file(path: str, file_path: str = "./pyproject.toml"):
    log.info("reading toml file")

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            toml_data = tomli.load(f)
    else:
        return None

    log.debug(toml_data)
    log.debug(path)

    return get_toml_path(toml_data, path)
