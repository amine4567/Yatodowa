import inspect
from functools import wraps
from typing import Callable

import pydantic
from flask import Blueprint, jsonify, request
from yatodowa_api.common.schemas import APICallError, ErrorType, StrictBaseModel
from yatodowa_api.consts import REQUEST_ARGS_KWARG, REQUEST_BODY_PARAM, RESERVED_KWARGS


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
                f"variables but are missing in {decorated_f}'s parameters."
            )

        if len(non_reserved_params - declared_url_vars) != 0:
            raise KeyError(
                f"{non_reserved_params - declared_url_vars} are declared in the "
                f"{decorated_f}'s parameters but are not declared as URL variables."
            )

        annotated_params = {
            k: (v, ...)
            for k, v in decorated_f.__annotations__.items()
            if k not in RESERVED_KWARGS
        }
        missing_annotations = declared_url_vars - set(annotated_params.keys())
        if len(missing_annotations) != 0:
            raise KeyError(
                f"{missing_annotations} are declared as URL variables, exist in the "
                f"{decorated_f}'s parameters but are missing annotations. Please add "
                "type hints to these parameters."
            )

        try:
            UrlVarsModel = pydantic.create_model(
                "UrlVarsModel", __base__=StrictBaseModel, **annotated_params
            )
            url_vars_values = request.view_args

            validated_values = UrlVarsModel(**url_vars_values)
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

        new_kwargs = {**kwargs, **validated_values.dict()}
        return decorated_f(*args, **new_kwargs)

    return modified_f


def validate_request_vals(
    param_name: str, request_vals_getter: Callable[[], dict]
) -> Callable:
    def decorator(decorated_f: Callable) -> Callable:
        @wraps(decorated_f)
        def modified_f(*args, **kwargs):
            if param_name in inspect.signature(decorated_f).parameters:
                try:
                    Schema = decorated_f.__annotations__[param_name]
                except KeyError:
                    raise KeyError(
                        f"The '{param_name}' parameter not found in {decorated_f}'s "
                        "annotations. Please add a type hint. "
                    )

                if not issubclass(Schema, pydantic.BaseModel):
                    raise TypeError(
                        f"The '{param_name}' parameter expected to be of type "
                        f"{pydantic.BaseModel} but got {Schema}."
                    )

                try:
                    request_vals = Schema(**request_vals_getter())
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

                new_kwargs = {**kwargs, param_name: request_vals}
            else:
                try:
                    StrictBaseModel(**request_vals_getter())
                except pydantic.ValidationError:
                    return (
                        APICallError(
                            type=ErrorType.VALIDATION,
                            message=f"{param_name} is expected to be empty but got "
                            + str(request_vals_getter()),
                        ),
                        400,
                    )

                new_kwargs = kwargs

            return decorated_f(*args, **new_kwargs)

        return modified_f

    return decorator


validate_request_body = validate_request_vals(
    REQUEST_BODY_PARAM, lambda: request.get_json() or dict()
)
validate_request_args = validate_request_vals(
    REQUEST_ARGS_KWARG, lambda: dict(request.args)
)


class ValidatedBlueprint(Blueprint):
    def route(self, *args, **kwargs):
        def decorator(decorated_f: Callable) -> Callable:
            modified_f = decorated_f

            modified_f = validate_request_args(modified_f)

            modified_f = validate_request_body(modified_f)

            modified_f = validate_url_vars(modified_f)

            modified_f = serialize_response(modified_f)

            modified_f = super(Blueprint, self).route(*args, **kwargs)(modified_f)

            return modified_f

        return decorator
