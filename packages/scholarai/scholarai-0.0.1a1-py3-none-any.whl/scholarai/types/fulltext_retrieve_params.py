# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["FulltextRetrieveParams"]


class FulltextRetrieveParams(TypedDict, total=False):
    pdf_id: Required[str]
    """id for PDF.

    Must begin with be one of `PDF_URL:some.url.com` or `PROJ:some_path`
    """

    chunk: int
    """chunk number to retrieve, defaults to 1"""
