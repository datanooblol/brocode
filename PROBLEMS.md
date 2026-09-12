# These are what problems I need to solve as a study.

## finding all skills' names

```python
from pathlib import Path

ROOT = Path(...)
skills = list((ROOT / "skills").rglob("SKILL.md"))
skills = [s.parent.name for s in skills]
```

## reading a specific skill's `SKILL.md`

```python
from pathlib import Path

ROOT = Path(...)
target_file = ROOT / "skills" / <skill-name> / "SKILL.md"
text = target_file.read_text()
```

## reading a specific skill's `references/*.md`

```python
from pathlib import Path

ROOT = Path(...)
target_file = ROOT / "skills" / <skill-name> / "references" / <reference-name>.md
text = target_file.read_text()
```

## reading a specific skill's `scripts/*.py`

```python
from pathlib import Path

ROOT = Path(...)
target_file = ROOT / "skills" / <skill-name> / "scripts" / <script-name>.py
text = target_file.read_text()
```

## solve if LLM needs more information in each turn

## solve if LLM needs to load a specific `references/*.md` file up.
