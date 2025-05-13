# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["EvaluateMetadataParams"]


class EvaluateMetadataParams(TypedDict, total=False):
    agent_id: Required[str]
    """Agent ID associated with the evaluation dataset"""

    version: str
    """Version number of the dataset. Defaults to the latest version if not specified."""
