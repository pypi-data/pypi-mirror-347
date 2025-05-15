# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["SaveCitationRetrieveResponse"]


class SaveCitationRetrieveResponse(BaseModel):
    message: Optional[str] = None
    """Confirmation of successful save or error message."""
