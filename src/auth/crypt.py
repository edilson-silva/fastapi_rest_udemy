from passlib.context import CryptContext


class Crypt:
    def __init__(self, password) -> None:
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.password = password

    def get_hashed_password(self):
        return self.__pwd_context.hash(self.password)
