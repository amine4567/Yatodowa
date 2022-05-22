from pydantic import validator


def validate_count(list_field: str, count_field: str = "count") -> classmethod:
    decorator = validator(count_field, allow_reuse=True, always=True)

    def compute_count(_, values: dict) -> int:
        return len(values[list_field])

    return decorator(compute_count)


def validate_text_length(max_len: int, text_field: str = "text") -> classmethod:
    decorator = validator(text_field, allow_reuse=True, always=True)

    def check_text_length(value: str | None):
        if value is not None and len(value) > max_len:
            raise ValueError(
                "Too many characters. Maximum accepted string length: " + str(max_len)
            )
        return value

    return decorator(check_text_length)
