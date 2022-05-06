from string import ascii_lowercase, ascii_uppercase, digits, punctuation


class PasswordValidatorSchema(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value) -> str:
        if len(value) < 8:
            raise ValueError("Password must be more than 8 digits")

        if not any(l in value for l in ascii_lowercase):
            raise ValueError("Password must contains at least one lower letter")

        if not any(l in value for l in ascii_uppercase):
            raise ValueError("Password must contains at least one upper letter")

        if not any(d in value for d in digits):
            raise ValueError("Password must contains at least one digit")

        if not any(p in value for p in punctuation):
            raise ValueError(
                f"Password must contains at least one special characters from: {punctuation}"
            )

        return value
