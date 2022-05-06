class NameValidatorSchema(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value) -> str:
        if len(value.split()) < 2:
            raise ValueError("Name must containers at least two words")

        return value
