"""
Константы для рас.
"""

from enum import Enum


class RaceType(Enum):
    """
    Тип расы.
    """

    human = "human"
    elf = "elf"
    dwarf = "dwarf"
    gnome = "gnome"
    druid = "druid"
    vampire = "vampire"
    demon = "demon"
