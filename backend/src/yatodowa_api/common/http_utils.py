import inspect
from functools import wraps
from typing import Callable

import pydantic
from flask import Blueprint, jsonify, request
from yatodowa_api.common.schemas import APICallError, CustomBaseModel, ErrorType
from yatodowa_api.consts import REQUEST_ARGS_KWARG, REQUEST_BODY_KWARG, RESERVED_KWARGS


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

    @wraps(decorated_f)
    def modified_f(*args, **kwargs):
        declared_url_vars = request.url_rule.arguments
        illegal_url_vars = declared_url_vars.intersection(RESERVED_KWARGS)
        if len(illegal_url_vars) != 0:
            raise KeyError(
                f"{illegal_url_vars} are reserved keywords and cannot be used as URL "
                "variables."
            )

        non_reserved_params = set(
            inspect.signature(decorated_f).parameters.keys()
        ) - set(RESERVED_KWARGS)
        if len(declared_url_vars - non_reserved_params) != 0:
            raise KeyError(
                f"{declared_url_vars - non_reserved_params} are declared as URL "
                "variables but are missing in the function's parameters."
            )

        if len(non_reserved_params - declared_url_vars) != 0:
            raise KeyError(
                f"{non_reserved_params - declared_url_vars} are declared in the "
                "function's parameters but are not declared as URL variables."
            )

        annotated_params = {
            k: (v, ...)  # TODO: what if the function's parameters have default values ?
            for k, v in decorated_f.__annotations__.items()
            if k not in RESERVED_KWARGS
        }
        missing_annotations = declared_url_vars - set(annotated_params.keys())
        if len(missing_annotations) != 0:
            raise KeyError(
                f"{missing_annotations} are declared as URL variables, exist in the "
                "function's parameters but are missing annotations. Please add type "
                "hints to these parameters."
            )

        try:
            UrlVarsModel = pydantic.create_model(
                "UrlVarsModel", __base__=CustomBaseModel, **annotated_params
            )
            url_vars_values = request.view_args

            validated_values = UrlVarsModel(**url_vars_values)
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

        new_kwargs = {**kwargs, **validated_values.dict()}
        return decorated_f(*args, **new_kwargs)

    return modified_f


def validate_request_vals(kwarg_name: str, request_vals_getter: Callable) -> Callable:
    def decorator(decorated_f: Callable) -> Callable:
        @wraps(decorated_f)
        def modified_f(*args, **kwargs):
            try:
                Schema = decorated_f.__annotations__[kwarg_name]
            except KeyError:
                raise KeyError(
                    f"The '{kwarg_name}' kwarg not found in {decorated_f}'s "
                    "annotations. Please make sure the kwarg exists with the correct "
                    "type hint."
                )

            if not issubclass(Schema, pydantic.BaseModel):
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
        def decorator(decorated_f: Callable) -> Callable:
            f_params = inspect.signature(decorated_f).parameters

            modified_f = decorated_f

            if REQUEST_ARGS_KWARG in f_params:
                # TODO: what if arguments are passed when they are not expected ?
                modified_f = validate_request_args(modified_f)

            if REQUEST_BODY_KWARG in f_params:
                # TODO: what if a request body is given even though it's not expected ?
                modified_f = validate_request_body(modified_f)

            modified_f = validate_url_vars(modified_f)

            modified_f = serialize_response(modified_f)

            modified_f = super(Blueprint, self).route(*args, **kwargs)(modified_f)

            return modified_f

        return decorator
