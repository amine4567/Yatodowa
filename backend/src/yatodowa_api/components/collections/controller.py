from uuid import UUID

import yatodowa_api.components.collections.service as CollectionService
import yatodowa_api.components.tasks.service as TaskService
from yatodowa_api.components.common.schemas import PaginationArgsModel
from yatodowa_api.consts import COMMON_API_PREFIX
from yatodowa_api.validation import APICallError, ErrorType, ValidatedBlueprint

from .exceptions import CollectionNotFoundError
from .schemas import CollectionPostQueryBodyModel, MultiCollectionsRespModel

collections_api = ValidatedBlueprint(
    "collections_api", __name__, url_prefix=COMMON_API_PREFIX + "/collections"
)


@collections_api.route("/", methods=["GET"])
def get_collections():
    collections = CollectionService.get_collections()
    return MultiCollectionsRespModel(collections=collections), 200


@collections_api.route("/", methods=["POST"])
def add_collection(request_body: CollectionPostQueryBodyModel):
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


@collections_api.route("/<collection_id>/tasks", methods=["GET"])
def get_collection_tasks(request_args: PaginationArgsModel, collection_id: UUID):
    try:
        tasks = TaskService.get_tasks(
            page_size=request_args.page_size,
            skip=request_args.skip,
            collection_id=collection_id,
        )
    except CollectionNotFoundError as e:
        return APICallError(type=ErrorType.MISSING_RESOURCE, message=str(e)), 400
    else:
        return tasks, 200
