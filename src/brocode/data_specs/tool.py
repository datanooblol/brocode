from dataclasses import dataclass
from pathlib import Path

@dataclass
class Arg:
    name: str
    type: str
    description: str | None = None
    required: bool | None = True

@dataclass
class Tool:
    name: str
    description: str
    args: list[Arg]
    path: Path
