# Create a skill extraction module that:
# - loads skills from data/skills.json
# - performs case-insensitive matching
# - avoids partial-word false positives (e.g. "C" in "CSS")
# - exposes extract_skills(text: str) -> list[str]
import json
import os
import re

_SKILLS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "skills.json")
_skills: list[str] | None = None


def _load_skills() -> list[str]:
    global _skills
    if _skills is None:
        with open(_SKILLS_PATH, encoding="utf-8") as f:
            _skills = json.load(f)
    return _skills


def extract_skills(text: str) -> list[str]:
    """Find skills from data/skills.json in text. Case-insensitive, whole-word only."""
    skills = _load_skills()
    found: list[str] = []
    for skill in skills:
        # Escape regex special chars in skill name, then wrap in word boundaries
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)
    return found
