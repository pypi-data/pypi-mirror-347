# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SaveCitationRetrieveParams"]


class SaveCitationRetrieveParams(TypedDict, total=False):
    doi: Required[str]
    """Digital Object Identifier (DOI) of the article"""

    zotero_api_key: Required[str]
    """Zotero API Key"""

    zotero_user_id: Required[str]
    """Zotero User ID"""
