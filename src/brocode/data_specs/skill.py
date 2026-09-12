from dataclasses import dataclass
from typing import List
from pathlib import Path
from enum import StrEnum

class SkillStatus(StrEnum):
    STABLE = 'stable'
    EXPERIMENT = 'experiment'
    DEPRECATED = 'deprecated'

@dataclass
class Skill:
    name:str
    description:str
    version:str
    path:Path
    tags:List[str] | None = None
    keywords:List[str] | None = None
    default:bool = False
    status:SkillStatus | None = SkillStatus.EXPERIMENT