from functools import wraps
from typing import Callable, Dict, List
from uuid import UUID

import pydantic
from flask import jsonify, request
from yatodowa_api.consts import REQUEST_BODY_KWARG


def validate_uuid_input(input_name: str, from_request: bool = False) -> Callable:
    def decorator_f(decorated_f: Callable) -> Callable:
        @wraps(decorated_f)
        def modified_f(*args, **kwargs):
            if from_request:
                inputs_dict = get_request_body(kwargs)
            else:
                inputs_dict = kwargs

            try:
                inputs_dict[input_name] = UUID(inputs_dict[input_name])
            except KeyError:
                source = f"'{REQUEST_BODY_KWARG}'" if from_request else "the kwargs"
                raise KeyError(
                    f"{decorated_f.__name__}: '{input_name}' not found in {source}"
                )
            except ValueError:
                return (
                    jsonify(
                        {
                            "error_message": f"{input_name} : "
                            f"{inputs_dict[input_name]} is not a valid hex UUID string"
                        }
                    ),
                    400,
                )

            return decorated_f(*args, **kwargs)

        return modified_f

    return decorator_f


def check_request_fields(mandatory_fields: List) -> Callable:
    def decorator_f(decorated_f: Callable) -> Callable:
        @wraps(decorated_f)
        def modified_f(*args, **kwargs):
            request_body = get_request_body(kwargs)
            try:
                missing_fields = set(mandatory_fields) - set(request_body.keys())
                assert len(missing_fields) == 0
            except AssertionError:
                return (
                    jsonify(
                        {
                            "error": "The following mandatory fields are missing: "
                            + str(missing_fields)
                        }
                    ),
                    400,
                )
            return decorated_f(*args, **kwargs)

        return modified_f

    return decorator_f


def inject_request_body(decorated_f: Callable) -> Callable:
    @wraps(decorated_f)
    def modified_f(*args, **kwargs):
        new_kwargs = {**kwargs, REQUEST_BODY_KWARG: request.get_json()}
        return decorated_f(*args, **new_kwargs)

    return modified_f


def get_request_body(func_kwargs: Dict) -> Dict:
    try:
        request_body = func_kwargs[REQUEST_BODY_KWARG]
    except KeyError:
        raise KeyError(
            f"'{REQUEST_BODY_KWARG}' not found in the function's kwargs. "
            + "Please inject it by decorating the function with "
            + f"'{inject_request_body.__name__}'."
        )
    else:
        return request_body


def validate_request(decorated_f: Callable) -> Callable:
    @wraps(decorated_f)
    def modified_f(*args, **kwargs):
        try:
            RequestSchema = decorated_f.__annotations__[REQUEST_BODY_KWARG]
            assert issubclass(RequestSchema, pydantic.BaseModel)
        except KeyError:
            raise KeyError(
                f"The '{REQUEST_BODY_KWARG}' kwarg not found in {decorated_f}'s "
                "annotations. Please make sure the kwarg exists with the correct type "
                "hint."
            )
        except AssertionError:
            raise TypeError(
                f"The '{REQUEST_BODY_KWARG}' kwarg expected to be of type "
                f"{pydantic.BaseModel} but got {RequestSchema}."
            )

        try:
            request_body = RequestSchema(**request.get_json())
        except pydantic.ValidationError as e:
            return jsonify({"validation_error": e.errors()}), 400

        new_kwargs = {**kwargs, REQUEST_BODY_KWARG: request_body}
        return decorated_f(*args, **new_kwargs)

    return modified_f
    
