"""
No FastAPI import in domain logic.
"""

import enum


class Permission(str, enum.Enum):
    USER_READ = "user:read"
    USER_DELETE = "user:delete"
    USER_UPDATE = "user:update"
    USER_LIST = "user:list"

    TASK_CREATE = "task:create"
    TASK_ASSIGN = "task:assign"
    TASK_DELETE = "task:delete"
