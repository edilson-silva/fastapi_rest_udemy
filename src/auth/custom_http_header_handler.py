from os import environ
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError, InvalidTokenError, decode
from src.connection.database import get_db_connection
from src.models.users import UserModel

from .token import TOKEN_ALGORITHM


class CustomHTTPHeaderHandler(HTTPBearer):
    def __init__(self):
        super().__init__()
        self.db = next(get_db_connection())

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        req = await super().__call__(request)

        try:
            payload = decode(
                req.credentials,
                key=environ.get("JWT_SECRET_KEY"),
                algorithms=[TOKEN_ALGORITHM],
            )

            user_id = payload.get("sub", -1)
            user = self.db.query(UserModel).filter(UserModel.id == user_id).first()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
                codes

            request.state.user = user

            return payload

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired"
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
