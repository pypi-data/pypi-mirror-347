# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["LedgerCreateOrderParams"]


class LedgerCreateOrderParams(TypedDict, total=False):
    claim_amount: Required[Annotated[str, PropertyInfo(alias="claimAmount")]]
    """Claim amount in cents"""

    claim_id: Required[Annotated[str, PropertyInfo(alias="claimId")]]
    """Claim ID"""

    institution_amount: Required[Annotated[str, PropertyInfo(alias="institutionAmount")]]
    """Institution amount in cents"""

    institution_id: Required[Annotated[str, PropertyInfo(alias="institutionId")]]
    """Institution ID"""

    insurance_id: Required[Annotated[str, PropertyInfo(alias="insuranceId")]]
    """Insurance ID. Insurance payment is grouped by insurance."""

    order_id: Required[Annotated[str, PropertyInfo(alias="orderId")]]
    """Order ID"""

    patient_amount: Required[Annotated[str, PropertyInfo(alias="patientAmount")]]
    """Patient amount in cents"""

    patient_id: Required[Annotated[str, PropertyInfo(alias="patientId")]]
    """Patient ID"""

    unallocated_amount: Required[Annotated[str, PropertyInfo(alias="unallocatedAmount")]]
    """Unallocated amount in cents"""
