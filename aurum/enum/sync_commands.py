from enum import Enum


class SyncCommandsFlag(Enum):
    """Defines the modes of synchronization for commands in the Discord API.

    Attributes:
        NONE (SyncCommandsFlag): Represents no synchronization.
        SYNC (SyncCommandsFlag): Represents synchronization process.
        DEBUG (SyncCommandsFlag): Represents synchronization process with debug information.
    """

    NONE = 0
    SYNC = 1
    DEBUG = 2
