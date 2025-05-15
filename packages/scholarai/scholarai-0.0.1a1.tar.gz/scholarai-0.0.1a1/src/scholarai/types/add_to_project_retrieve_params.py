# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AddToProjectRetrieveParams"]


class AddToProjectRetrieveParams(TypedDict, total=False):
    paper_id: Required[str]
    """
    Identifier of the paper to add, must be of the format
    <identifier_type>:<identifier_value>. Identifier type can be one of DOI, PMID,
    SS_ID, ARXIV, MAG, ACL, or PMCID.
    """

    project_id: str
    """The project ID to which the items are being added. Default to 'gpt'"""

    project_name: str
    """The project name to which the items are being added. Alternative to project_id"""
