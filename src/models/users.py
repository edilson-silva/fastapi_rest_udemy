from sqlalchemy import Column, Enum, Integer, String
from src.connection.database import Base
from src.util.user_roles import UserRoles


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRoles), nullable=False)
