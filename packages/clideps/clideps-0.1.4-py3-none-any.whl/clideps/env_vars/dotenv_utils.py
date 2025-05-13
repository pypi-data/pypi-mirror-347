import os
from pathlib import Path
from shutil import copyfile

from dotenv import find_dotenv, load_dotenv
from dotenv.main import DotEnv, rewrite, with_warn_for_invalid_lines
from dotenv.parser import parse_stream

DOTENV_NAMES = [".env", ".env.local"]


def find_dotenv_paths(include_home: bool = True, *extra_dirs: Path) -> list[Path]:
    """
    Find .env or .env.local files in the current directory and return a list of
    paths. If extra_dirs are provided, they will be checked for .env or
    .env.local files as well.
    """
    # First check up the current directory hierarchy.
    path_strs = [find_dotenv(filename=filename, usecwd=True) for filename in DOTENV_NAMES]
    paths = [Path(p).expanduser().resolve() for p in path_strs if p]

    # Now check home and any other extras.
    dir_list = list(extra_dirs or [])
    if include_home:
        dir_list.append(Path.home())
    for dir in dir_list:
        for filename in DOTENV_NAMES:
            path = (dir / filename).expanduser().resolve()
            if path.exists() and path not in paths:
                paths.append(path)

    return paths


def load_dotenv_paths(
    override: bool = True, include_home: bool = True, *extra_dirs: Path
) -> list[Path]:
    """
    Find and load .env orfiles.
    """
    dotenv_paths = find_dotenv_paths(include_home, *extra_dirs)
    for dotenv_path in dotenv_paths:
        load_dotenv(dotenv_path, override=override)
    return dotenv_paths


def read_dotenv_file(dotenv_path: str | Path) -> dict[str, str | None]:
    """
    Read a .env file and return a dictionary of key-value pairs.
    """
    return DotEnv(dotenv_path=dotenv_path).dict()


def env_var_is_set(key: str, min_length: int = 10, forbidden_str: str = "changeme") -> bool:
    """
    Check if an environment variable is set and plausible (not a dummy or empty value).
    """
    value = os.environ.get(key, None)
    return bool(
        value and len(value.strip()) > min_length and forbidden_str.lower() not in value.lower()
    )


def update_env_file(
    dotenv_path: Path,
    updates: dict[str, str],
    create_if_missing: bool = False,
    backup_suffix: str | None = ".bak",
) -> tuple[list[str], list[str]]:
    """
    Updates values in a .env file (safely). Similar to what dotenv offers but allows multiple
    updates at once and keeps a backup. Values may be quoted or unquoted.
    """
    if not create_if_missing and not dotenv_path.exists():
        raise FileNotFoundError(f".env file does not exist: {dotenv_path}")

    # Create the .env file directory if it doesn't exist
    if create_if_missing and not dotenv_path.parent.exists():
        dotenv_path.parent.mkdir(parents=True, exist_ok=True)

    def format_line(key: str, value: str) -> str:
        if (value.startswith("'") and value.endswith("'")) or (
            value.startswith('"') and value.endswith('"')
        ):
            return f"{key}={value}"
        else:
            return f"{key}=" + '"' + value.replace('"', '\\"') + '"'

    if backup_suffix and dotenv_path.exists():
        copyfile(dotenv_path, dotenv_path.with_name(dotenv_path.name + backup_suffix))

    changed: list[str] = []
    added: list[str] = []
    with rewrite(dotenv_path, encoding="utf-8") as (source, dest):
        for mapping in with_warn_for_invalid_lines(parse_stream(source)):
            if mapping.key in updates:
                dest.write(format_line(mapping.key, updates[mapping.key]))
                dest.write("\n")
                changed.append(mapping.key)
            else:
                dest.write(mapping.original.string.rstrip("\n"))
                dest.write("\n")
        for key in set(updates.keys()) - set(changed):
            dest.write(format_line(key, updates[key]))
            dest.write("\n")
            added.append(key)

    return changed, added
