from yatodowa_api.validation import StrictBaseModel


class PaginationArgsModel(StrictBaseModel):
    page_size: int = 100
    skip: int = 0
