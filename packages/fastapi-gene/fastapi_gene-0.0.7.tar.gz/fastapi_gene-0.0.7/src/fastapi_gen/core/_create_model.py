import asyncio
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, TypedDict, Union

import httpx
from httpx import HTTPStatusError

from fastapi_gen.exceptions import DirectoryNotFound, ModuleNotSupported

from .action import save_to_file


class RequiredFile(TypedDict):
    file_name: str
    subdir: str


RequiredDirType = Tuple[str, str, str]

REPO_OWNER = "fastapi-users"
FILE_EXTENSION = ".py"
SUPPORTED_MODULES: Dict[str, str] = {
    "fastapi-users[sqlalchemy]": "sqlalchemy",
    "fastapi-users[sqlalchemy,oauth]": "sqlalchemy-oauth",
    "fastapi-users[beanie]": "beanie",
    "fastapi-users[beanie,oauth]": "beanie-oauth",
}
REQUIRED_DIRS: RequiredDirType = ("models", "schema", "api")
REQUIRED_FILES: Tuple[RequiredFile, ...] = (
    {"file_name": "app", "subdir": "api"},
    {"file_name": "schemas", "subdir": "schema"},
    {"file_name": "db", "subdir": "models"},
    {"file_name": "users", "subdir": "models"},
)


def format_model_name(model: str) -> str:
    if model not in SUPPORTED_MODULES:
        raise ModuleNotSupported(f"Unsupported module: '{model}'")
    return SUPPORTED_MODULES[model]


def check_required_dirs(
    path: Path, dirs: RequiredDirType, skip: bool = True
) -> Optional[Path]:
    for dir_name in dirs:
        sub_path = path / dir_name
        if not sub_path.is_dir():
            if skip:
                return None
            expected = ", ".join(dirs)
            raise DirectoryNotFound(
                f"'{expected}' should be present inside '{path}' or attach '--default' "
            )
    return path


def save_to_path(
    filename: str, targetpath: Path, response: str, extension: str = FILE_EXTENSION
) -> None:
    file_path = targetpath / f"{filename}{extension}"
    file_path.write_text(response, encoding="utf-8")


async def fetch_and_save_file(
    client: httpx.AsyncClient,
    base_url: str,
    file_meta: Dict[str, Any],
    container: Dict[str, str],
    default: bool,
):
    filename = file_meta["file_name"]
    subdir = file_meta["path"]
    url = f"{base_url}{filename}{FILE_EXTENSION}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        if default:
            save_to_path(filename, file_meta["current"], response.text)
        else:
            save_to_file(subdir, filename, FILE_EXTENSION, response, container)
    except HTTPStatusError as e:
        raise RuntimeError(
            f"Failed to fetch '{filename}' from '{url}': HTTP {e.response.status_code}"
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"Unexpected error while fetching '{filename}' from '{url}': {e}"
        ) from e


async def generate_model(formatted_module: str, save_dir: Optional[str], default: bool):
    base_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_OWNER}/master/examples/{formatted_module}/app/"
    target_path = Path(save_dir or Path.cwd()).expanduser().resolve()

    if not target_path.exists():
        raise DirectoryNotFound(
            f"Destination directory '{target_path}' does not exist."
        )

    model_root: Union[Path, None] = check_required_dirs(target_path, REQUIRED_DIRS)

    if not model_root and not default:
        subdirs = [
            d
            for d in target_path.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]
        if not subdirs:
            raise DirectoryNotFound(
                "Expecting at least 'One valid' subdirectory in target directory."
            )
        model_root = check_required_dirs(subdirs[0], REQUIRED_DIRS, skip=False)

    if default:
        model_root = target_path
        response = """
        Create a (app) directory and move all generate files into it

        """
        save_to_path("instruction.txt", model_root, response, extension=".txt")
    init_container: Dict[str, str] = {}
    assert model_root is not None
    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_and_save_file(
                client,
                base_url,
                {**f, "path": model_root / f["subdir"], "current": model_root},
                init_container,
                default,
            )
            for f in REQUIRED_FILES
        ]
        await asyncio.gather(*tasks)

    # Append imports to __init__.py files
    for key, content in init_container.items():
        dir_name = "models" if key == "db" else key
        init_path = model_root / dir_name / f"__init__{FILE_EXTENSION}"
        if key == "models":
            content = content.replace("from .users import User", "")
        with open(init_path, "a", encoding="utf-8") as f:
            f.write(content)


def create_model(model: str, target: str | None = None, default: bool = False):
    formatted_module = format_model_name(model)
    asyncio.run(generate_model(formatted_module, target, default))
