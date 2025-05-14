from .strata_base_exception import (
    StrataBaseException,
)


class BackendException(StrataBaseException):
    """Domain exception for backend errors"""

    ...


class NotFoundException(StrataBaseException):
    """Domain exception for file/folder not found errors"""

    ...
