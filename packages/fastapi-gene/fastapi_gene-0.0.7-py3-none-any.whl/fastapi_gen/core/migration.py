import sys
from typing import Optional, Union

from alembic.command import (
    downgrade as func_downgrade,
    init as func_init,
    revision as func_revision,
    upgrade as func_upgrade,
)
from alembic.config import Config

from fastapi_gen.exceptions import FastapiGen
from fastapi_gen.utils.stdout_patch import RichStdout

DEFAULT_INI_FILE = "alembic.ini"


class Migration:
    def __init__(self, ini_file: str = DEFAULT_INI_FILE):
        self.config: Config = Config(file_=ini_file)
        self.upgrade_revision = "head"
        self.downgrade_revision = "base"

    def _colorize_stdout(self):
        sys.stdout = RichStdout()

    def _revision_setter(self, action: str, revision: str) -> None:
        migrate_cmd = f"{action}grade_revision"
        if revision and hasattr(self, migrate_cmd):
            setattr(self, migrate_cmd, revision)

    def makemigrations(
        self, init: bool, name: str, autogenerate: bool, message: str | None = None
    ) -> None:
        """
        Handle migration creation:
        - If `init` is True, initializes a new Alembic environment.
        - Otherwise, creates a migration files.
        """
        self._colorize_stdout()
        if init:
            func_init(self.config, name)
        else:
            func_revision(self.config, message=message, autogenerate=autogenerate)

    def migrate(self, action: str, revision: str) -> None:
        """
        Apply or rollback migrations based on the action.
        """
        self._revision_setter(action, revision)
        self._colorize_stdout()
        if action == "up":
            func_upgrade(self.config, self.upgrade_revision)
        elif action == "down":
            func_downgrade(self.config, self.downgrade_revision)
        else:
            raise FastapiGen(f"Unknown action '{action}'. Must be 'up' or 'down'.")


def migrations_and_migrate(*args: Optional[Union[str, bool]], command: str) -> None:
    """
    Dispatcher for migration-related commands.
    """
    migration = Migration()

    if hasattr(migration, command):
        method = getattr(migration, command)
        if callable(method):
            method(*args)
        else:
            raise FastapiGen(f"Attribute '{command}' is not callable.")
    else:
        raise FastapiGen(f"'Migration' object has no command '{command}'.")
