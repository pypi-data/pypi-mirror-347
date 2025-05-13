from enum import Enum


class MigrationGrade(str, Enum):
    upgrade = "up"
    downgrade = "down"
