import yatodowa_api.components.collections.service as CollectionService
from yatodowa_api.api_validation import APICallError, ErrorType, ValidatedBlueprint
from yatodowa_api.consts import COMMON_API_ENDPOINT

from .schemas import CollectionQueryBody, CollectionsResponse

collections_api = ValidatedBlueprint("collections_api", __name__)


@collections_api.route(COMMON_API_ENDPOINT + "/collections", methods=["GET"])
def get_collections():
    collections = CollectionService.get_collections()
    return CollectionsResponse(count=len(collections), collections=collections), 200


@collections_api.route(COMMON_API_ENDPOINT + "/collections", methods=["POST"])
def add_collection(request_body: CollectionQueryBody):
    existing_collections_names = [
        elt.name for elt in CollectionService.get_collections()
    ]

    if request_body.name in existing_collections_names:
        return (
            APICallError(
                type=ErrorType.GENERIC,
                message="There already exist a collection with the name "
                + request_body.name,
            ),
            400,
        )

    collection = CollectionService.add_collection(request_body)

    return collection, 201
