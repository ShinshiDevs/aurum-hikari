import enum


class BucketType(int, enum.Enum):
    USER = 0
    MEMBER = 1
    GUILD = 2
