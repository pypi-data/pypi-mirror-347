import re
from pathlib import Path
from typing import Dict

import httpx

REPLACEMENTS = {
    "app": {
        "patterns": [
            (r"from contextlib import asynccontextmanager\n\n?", ""),
            (r", create_db_and_tables", ""),
            (r"from app\.db", "from {name}.models"),
            (r"from app\.schemas", "from {name}.schema"),
            (r"from app\.users", "from {name}.models"),
            (
                r"@asynccontextmanager\s+async def lifespan\(.*?\):\s+(.*?)\s+yield\n?",
                "",
                re.DOTALL,
            ),
            (
                r"from fastapi import (.*?)FastAPI",
                r"from fastapi import APIRouter,Depends",
            ),
            (r"app = FastAPI\(.*?\)", "user_router = APIRouter()"),
            (r"app\.include_router\(", "user_router.include_router("),
            (r"@app\.get\(", "@user_router.get("),
        ]
    },
    "db": {
        "patterns": [
            (r"test\.db", "fastgen.db"),
        ]
    },
    "users": {
        "patterns": [
            (r"from app.db", "from .db"),
        ]
    },
}


def _update_imports_for_init(
    grandparent: str, target_file: str, content: str, container: Dict[str, str]
):
    lines = content.splitlines()
    multi_line = False
    submodule = ""

    for line in lines:
        stripped = line.strip()

        if multi_line:
            container[submodule] += f"\n{stripped}"
            if stripped.endswith(")"):
                multi_line = False
            continue

        match = re.match(rf"^from {grandparent}\.(\w+) import(?:\s|\().*", stripped)
        if match:
            submodule = match.group(1)
            converted = stripped.replace(
                f"from {grandparent}.{submodule}", f"from .{target_file}"
            )
            container.setdefault(submodule, "")
            container[submodule] += f"\n{converted}"
            if stripped.endswith("("):
                multi_line = True
            continue

        match = re.match(r"^from \.(\w+) import(?:\s|\().*", stripped)
        if match:
            submodule = match.group(1)
            container[submodule] = f"\n{stripped}"


def _apply_replacements(module_name: str, filename: str, text: str) -> str:
    config = REPLACEMENTS.get(filename)
    if not config:
        return text

    for pattern, replacement, *flags in config["patterns"]:
        text = re.sub(
            pattern,
            replacement.format(name=module_name),
            text,
            flags=flags[0] if flags else 0,
        )
    return text


def save_to_file(
    dir_path: Path,
    filename: str,
    extension: str,
    response: httpx.Response,
    container: Dict[str, str],
):
    parent_dir = dir_path.parent.name
    target_file = "users" if filename != "db" else filename
    file_path = dir_path / f"{target_file}{extension}"

    modified_content = _apply_replacements(parent_dir, filename, response.text)
    file_path.write_text(modified_content, encoding="utf-8")

    _update_imports_for_init(parent_dir, target_file, modified_content, container)

    # Write __init__.py for `app` only
    if filename == "app":
        init_path = dir_path / f"__init__{extension}"
        with open(init_path, "a", encoding="utf-8") as f:
            f.write("\nfrom .users import user_router")
