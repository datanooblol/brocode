from pathlib import Path

def find_root(start: Path | None = None, marker: str = "skills") -> Path:
    """Walk upward from `start` (default: cwd) looking for a folder
    containing `marker`, the same trick git uses for `.git`.

    Args:
        start (Path): Where to begin the search. Defaults to Path.cwd().
        marker (str): Folder name that identifies the project root.

    Returns:
        Path: The first ancestor (including `start`) containing `marker/`.

    Raises:
        ValueError: If no ancestor contains `marker/`.
    """
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / marker).is_dir():
            return candidate
    raise ValueError(f"No '{marker}/' folder found in {current} or any parent")
