class PermissionDenied(Exception):
    """Raised when user is not allowed to perform an operation."""
    pass


class NotFound(Exception):
    """Optional: domain-level not found exception."""
    pass

class UserAlreadyExistsError(Exception):
    """Raised when trying to create a user that already exists."""
    pass