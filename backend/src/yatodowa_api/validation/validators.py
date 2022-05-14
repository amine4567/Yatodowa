from pydantic import validator


def count_validator(list_field: str, count_field: str = "count") -> classmethod:
    decorator = validator(count_field, allow_reuse=True, always=True)

    def compute_count(_, values: dict) -> int:
        return len(values[list_field])

    return decorator(compute_count)
