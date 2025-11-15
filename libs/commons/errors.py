class ValidationError(Exception):
    """User/input validation error."""


class DomainError(Exception):
    """Business rule violation."""


class InfraError(Exception):
    """Infrastructure/adapter failure."""