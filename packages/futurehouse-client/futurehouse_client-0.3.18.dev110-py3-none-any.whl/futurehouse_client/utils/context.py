from typing import Any, ClassVar

USER_JWT_CONTEXT_KEY = "user_jwt"
JOB_ID_CONTEXT_KEY = "job_id"


class RequestContext:
    """A context manager for storing information from the initial request."""

    _context: ClassVar[dict[str, Any]] = {}

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """Set a context variable.

        Args:
            key: The context variable name
            value: The value to store
        """
        cls._context[key] = value

    @classmethod
    def get(cls, key: str) -> Any:
        """Get a context variable.

        Args:
            key: The context variable name
            default: Default value if key doesn't exist

        Returns:
            The stored value or default if not found
        """
        return cls._context.get(key, None)

    @classmethod
    def clear(cls, key: str | None = None) -> None:
        """Clear a specific context variable or all variables.

        Args:
            key: Specific key to clear, or None to clear all
        """
        if key is None:
            cls._context.clear()
        elif key in cls._context:
            del cls._context[key]
