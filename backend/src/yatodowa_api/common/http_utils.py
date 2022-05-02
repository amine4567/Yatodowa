import inspect
from functools import wraps
from typing import Callable

import pydantic
from flask import Blueprint, jsonify, request
from yatodowa_api.common.schemas import APICallError, ErrorType
from yatodowa_api.consts import REQUEST_ARGS_KWARG, REQUEST_BODY_KWARG


def serialize_response(decorated_f: Callable) -> Callable:
    @wraps(decorated_f)
    def modified_f(*args, **kwargs):
        response, response_code = decorated_f(*args, **kwargs)
        # TODO: assert on reponse type
        if isinstance(response, list):
            return jsonify([elt.dict() for elt in response]), response_code
        else:
            return jsonify(response.dict()), response_code

    return modified_f


def validate_url_vars(decorated_f: Callable) -> Callable:
    """decorator to validate an URL variable as defined by flask using pydantic
    Example: http://127.0.0.1:5000/api/v1/tasks/408bce1f-f36e-4d39-9d69-614071572d84

    Args:
        decorated_f (Callable): _description_

    Returns:
        Callable: _description_
    """
    # TODO: remove check on REQUEST_ARGS_KWARG and REQUEST_BODY_KWARG
    @wraps(decorated_f)
    def modified_f(*args, **kwargs):
        try:
            validated_f = pydantic.validate_arguments(decorated_f)
            validated_f.validate(*args, **kwargs)
        except pydantic.ValidationError as e:
            print(e.errors())
            return (
                [
                    APICallError(
                        type=ErrorType.VALIDATION,
                        subtype=error["type"],
                        message=".".join(error["loc"]) + ": " + error["msg"],
                    )
                    for error in e.errors()
                ],
                400,
            )

        return validated_f(*args, **kwargs)

    return modified_f


def validate_request_vals(kwarg_name: str, request_vals_getter: Callable) -> Callable:
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
                return (
                    [
                        APICallError(
                            type=ErrorType.VALIDATION,
                            subtype=error["type"],
                            message=".".join(error["loc"]) + ": " + error["msg"],
                        )
                        for error in e.errors()
                    ],
                    400,
                )

            new_kwargs = {**kwargs, kwarg_name: request_args}
            return decorated_f(*args, **new_kwargs)

        return modified_f

    return decorator


validate_request_body = validate_request_vals(
    REQUEST_BODY_KWARG, lambda: request.get_json()
)
validate_request_args = validate_request_vals(REQUEST_ARGS_KWARG, lambda: request.args)


class ValidatedBlueprint(Blueprint):
    def route(self, *args, **kwargs):
        # TODO: add validate_request_vals
        def decorator(decorated_f: Callable) -> Callable:
            f_params = inspect.signature(decorated_f).parameters

            modified_f = decorated_f

            modified_f = validate_url_vars(modified_f)

            if REQUEST_ARGS_KWARG in f_params:
                modified_f = validate_request_args(modified_f)

            if REQUEST_BODY_KWARG in f_params:
                modified_f = validate_request_body(modified_f)

            modified_f = serialize_response(modified_f)

            modified_f = super(Blueprint, self).route(*args, **kwargs)(modified_f)

            return modified_f

        return decorator
