from email_validator import EmailNotValidError, validate_email


class EmailValidatorSchema(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value) -> str:
        try:
            value = value.strip().lower()
            validate_email(value)
            return value
        except EmailNotValidError:
            raise ValueError("Invalid email")
