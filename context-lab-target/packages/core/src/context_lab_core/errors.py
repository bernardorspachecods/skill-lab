class DomainError(Exception):
    """Base class for expected domain failures."""


class NotFound(DomainError):
    """A requested domain object does not exist."""


class PermissionDenied(DomainError):
    """The actor is not allowed to perform the requested operation."""
