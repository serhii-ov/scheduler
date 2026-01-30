from app.users.roles import UserRole
from app.users.permissions import Permission


ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.ADMIN: {
        Permission.USER_READ,
        Permission.USER_DELETE,
        Permission.USER_UPDATE,
        Permission.TASK_CREATE,
        Permission.TASK_ASSIGN,
        Permission.TASK_DELETE,
        Permission.USER_LIST,
    },
    UserRole.ENGINEER: {
        Permission.USER_READ,
        Permission.USER_UPDATE,
        Permission.TASK_CREATE,
        Permission.TASK_ASSIGN,
        Permission.USER_LIST,
    },
    UserRole.ELECTRICIAN: {
        # Permission.USER_READ,
        Permission.TASK_CREATE,
    },
}
