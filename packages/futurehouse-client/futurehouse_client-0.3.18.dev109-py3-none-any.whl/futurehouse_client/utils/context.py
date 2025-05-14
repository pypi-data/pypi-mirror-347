class UserContext:
    """A context manager for storing user information from the initial request."""

    _user_jwt = None

    @classmethod
    def set_user_jwt(cls, jwt: str) -> None:
        cls._user_jwt = jwt

    @classmethod
    def get_user_jwt(cls) -> str | None:
        return cls._user_jwt

    @classmethod
    def clear_user_jwt(cls) -> None:
        cls._user_jwt = None
