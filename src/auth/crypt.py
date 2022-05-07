from passlib.context import CryptContext


class Crypt:
    def __init__(self) -> None:
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hashed_password(self, password: str) -> str:
        """Get password as a hash

        Args:
            password (str): Plain text password

        Returns:
            str: Password hashed string
        """
        return self.__pwd_context.hash(password)
