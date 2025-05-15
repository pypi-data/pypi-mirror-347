# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["AnalyzeProjectBatchAnalyzeParams"]


class AnalyzeProjectBatchAnalyzeParams(TypedDict, total=False):
    analysis_mode: Required[str]
    """The mode of analysis, options are 'comprehensive' and 'tabular'.

    Default to `tabular`.
    """

    project_name: Required[str]
    """The name of the project to analyze."""

    question: Required[List[str]]
    """Questions to analyze within the project."""
