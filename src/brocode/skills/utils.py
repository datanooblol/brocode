from pathlib import Path
from brocode.data_specs.skill import Skill
import re
import yaml

def split_frontmatter(text: str) -> tuple[dict, str]:
    """Split a SKILL.md file's text into its frontmatter and body.

    Args:
        text (str): Raw file contents, expected to start with a `---`
            delimited YAML block followed by the markdown body.

    Returns:
        tuple[dict, str]: The parsed frontmatter as a dict, and the
            remaining body text with surrounding whitespace stripped.

    Raises:
        ValueError: If no `---` delimited frontmatter block is found.
    """
    match = re.match(r'^---\n(.*?)\n---\n?(.*)', text, re.S)
    if not match:
        raise ValueError('No frontmatter block found')
    metadata = yaml.safe_load(match.group(1)) or {}
    body = match.group(2).strip()
    return metadata, body

def _load_skill(name: str, path:Path) -> Skill:
    """Load a single skill's frontmatter into a Skill instance.

    Args:
        name (str): The skill's folder name under `path`.
        path (Path): The skills root directory containing `name/SKILL.md`.

    Returns:
        Skill: The skill's metadata, with `path` set to its folder.

    Raises:
        ValueError: If `path/name/SKILL.md` does not exist.
    """
    SKILL_PATH = path / name / "SKILL.md"
    if not SKILL_PATH.is_file():
        raise ValueError(f"Skill {name} not found")
    metadata, _ = split_frontmatter(SKILL_PATH.read_text())
    return Skill(**metadata, path=path / name)

def load_skill_body(skill: Skill) -> str:
    """Load a skill's markdown body, i.e. the instructions below the frontmatter.

    Args:
        skill (Skill): The skill to load the body for.

    Returns:
        str: The body text, with surrounding whitespace stripped.
    """
    _, body = split_frontmatter((skill.path / "SKILL.md").read_text())
    return body

def load_script(skill: Skill)->list[Path]:
    """List a skill's executable scripts.

    Args:
        skill (Skill): The skill to inspect.

    Returns:
        list[Path]: Paths to every `*.py` file under the skill's `scripts/` folder.
    """
    return list(skill.path.glob("scripts/*.py"))

def load_reference(skill: Skill)->list[Path]:
    """List a skill's reference documents.

    Args:
        skill (Skill): The skill to inspect.

    Returns:
        list[Path]: Paths to every `*.md` file under the skill's `references/` folder.
    """
    return list(skill.path.glob("references/*.md"))

def load_asset(skill: Skill)->list[Path]:
    """List a skill's asset files.

    Args:
        skill (Skill): The skill to inspect.

    Returns:
        list[Path]: Paths to every `*.md` file under the skill's `assets/` folder.
    """
    return list(skill.path.glob("assets/*.md"))

def list_skills(path:Path)->list[Skill]:
    """List all skills under a root directory.

    Args:
        path (Path): Project root directory containing a `skills/` folder.

    Returns:
        list[Skill]: Every skill discovered by scanning `path/skills` for
            `SKILL.md` files.
    """
    skill_dir = path / "skills"
    skills = list(skill_dir.rglob("SKILL.md"))
    skills = [_load_skill(s.parent.name, skill_dir) for s in skills]
    return skills