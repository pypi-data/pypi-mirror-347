# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .paper_metadata import PaperMetadata

__all__ = ["AbstractSearchResponse"]

AbstractSearchResponse: TypeAlias = List[PaperMetadata]
