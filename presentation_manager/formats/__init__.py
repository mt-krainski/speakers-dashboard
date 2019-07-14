from .formats import (
    validate_format,
    BasePresentationFormat,
    get_format_hash_from_file,
    _get_hash,
)

FORMATS = {_get_hash(f): f for f in BasePresentationFormat.__subclasses__()}

FORMATS_CHOICES = [
    (_get_hash(f), f.get_name_display())
    for f in BasePresentationFormat.__subclasses__()
]

__all__ = (
    "validate_format",
    "get_format_hash_from_file",
    "FORMATS",
    "FORMATS_CHOICES",
)
