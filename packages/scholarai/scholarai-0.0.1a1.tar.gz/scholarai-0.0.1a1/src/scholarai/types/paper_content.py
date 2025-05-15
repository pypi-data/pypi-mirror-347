# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["PaperContent", "Chunk"]


class Chunk(BaseModel):
    chunk: Optional[str] = None

    chunk_num: Optional[int] = None

    img_mds: Optional[List[str]] = None

    pdf_url: Optional[str] = None


class PaperContent(BaseModel):
    chunks: Optional[List[Chunk]] = None

    hint: Optional[str] = None

    total_chunk_num: Optional[int] = None
