"""
Константы для скиллов.
"""

from enum import StrEnum


class SkillType(StrEnum):
    """
    Тип скилла.
    """

    active = "active"
    passive = "passive"
