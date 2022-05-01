from functools import wraps
from typing import Callable

import pydantic
from flask import jsonify, request
from yatodowa_api.consts import REQUEST_ARGS_KWARG, REQUEST_BODY_KWARG


def validate_url_vars(decorated_f: Callable) -> Callable:
    @wraps(decorated_f)
    def modified_f(*args, **kwargs):
        try:
            validated_f = pydantic.validate_arguments(decorated_f)
            validated_f.validate(*args, **kwargs)
        except pydantic.ValidationError as e:
            return jsonify({"validation_error": e.errors()}), 400

        return validated_f(*args, **kwargs)

    return modified_f


def validate_request_vals(kwarg_name: str, request_vals_getter: Callable):
    def decorator(decorated_f: Callable) -> Callable:
        @wraps(decorated_f)
        def modified_f(*args, **kwargs):
            try:
                Schema = decorated_f.__annotations__[kwarg_name]
                assert issubclass(Schema, pydantic.BaseModel)
            except KeyError:
                raise KeyError(
                    f"The '{kwarg_name}' kwarg not found in {decorated_f}'s "
                    "annotations. Please make sure the kwarg exists with the correct "
                    "type hint."
                )
            except AssertionError:
                raise TypeError(
                    f"The '{kwarg_name}' kwarg expected to be of type "
                    f"{pydantic.BaseModel} but got {Schema}."
                )

            try:
                request_args = Schema(**request_vals_getter())
            except pydantic.ValidationError as e:
                return jsonify({"validation_error": e.errors()}), 400

            new_kwargs = {**kwargs, kwarg_name: request_args}
            return decorated_f(*args, **new_kwargs)

        return modified_f

    return decorator


validate_request_body = validate_request_vals(
    REQUEST_BODY_KWARG, lambda: request.get_json()
)
validate_request_args = validate_request_vals(REQUEST_ARGS_KWARG, lambda: request.args)
