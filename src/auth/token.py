from datetime import datetime, timedelta
from os import environ

from jwt import encode as jwt_encode
from src.schemas.users import UserSchema

TOKEN_ALGORITHM = "HS256"


def generate_token(user: UserSchema) -> str:
    """Generate a new token based on user data

    Args:
        user (UserSchema): Source of token data

    Returns:
        str: The new token
    """
    try:
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(minutes=5)}
        return jwt_encode(
            payload=payload,
            key=environ.get("JWT_SECRET_KEY"),
            algorithm=TOKEN_ALGORITHM,
        )
    except Exception:
        raise Exception(message="Token generation error")
