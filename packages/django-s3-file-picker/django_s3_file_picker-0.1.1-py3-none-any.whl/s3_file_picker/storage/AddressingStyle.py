from enum import Enum


class AddressingStyle(Enum):
    PATH = "path"
    VIRTUAL_DOMAIN = "virtual"
    AUTO = "auto"
