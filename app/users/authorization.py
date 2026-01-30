"""
✔ No FastAPI
✔ No database
✔ Pure business logic
"""

from app.users.models import User
from app.users.permissions import Permission
from app.users.rbac import ROLE_PERMISSIONS
from app.users.exceptions import PermissionDenied


def has_permission(user: User, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS.get(user.role, set())


def require_owner_or_permission(
        *,
        current_user: User,
        target_user: User,
        permission: Permission,
    ) -> None:
    if current_user.id == target_user.id:
        return

    if has_permission(current_user, permission):
        return

    raise PermissionDenied("Operation not allowed")

