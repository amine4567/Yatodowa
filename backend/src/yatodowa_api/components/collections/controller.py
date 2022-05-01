import yatodowa_api.components.collections.service as CollectionService
from flask import Blueprint, jsonify
from yatodowa_api.common.http_utils import validate_request_body
from yatodowa_api.consts import COMMON_API_ENDPOINT

from .schemas import CollectionQueryBody

collections_api = Blueprint("collections_api", __name__)


@collections_api.route(COMMON_API_ENDPOINT + "/collections", methods=["GET"])
def get_collections():
    collections = CollectionService.get_collections()
    return jsonify([elt.to_dict() for elt in collections]), 200


@collections_api.route(COMMON_API_ENDPOINT + "/collections", methods=["POST"])
@validate_request_body
def add_collection(request_body: CollectionQueryBody):
    existing_collections_names = [
        elt.name for elt in CollectionService.get_collections()
    ]
    try:
        assert request_body.name not in existing_collections_names
    except AssertionError:
        return (
            jsonify(
                {
                    "error": "There already exist a collection with the name "
                    + request_body.name
                }
            ),
            400,
        )

    task = CollectionService.add_collection(
        name=request_body.name,
        group_id=request_body.group_id,
    )

    return (
        jsonify(
            {
                "result": "A new collection was created successfully.",
                "description": task.to_dict(),
            }
        ),
        201,
    )
