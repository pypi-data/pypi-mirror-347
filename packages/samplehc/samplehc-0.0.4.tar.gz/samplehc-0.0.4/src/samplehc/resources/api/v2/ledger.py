# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.api.v2 import ledger_create_order_params

__all__ = ["LedgerResource", "AsyncLedgerResource"]


class LedgerResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LedgerResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return LedgerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LedgerResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return LedgerResourceWithStreamingResponse(self)

    def create_order(
        self,
        *,
        claim_amount: str,
        claim_id: str,
        institution_amount: str,
        institution_id: str,
        insurance_id: str,
        order_id: str,
        patient_amount: str,
        patient_id: str,
        unallocated_amount: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Args:
          claim_amount: Claim amount in cents

          claim_id: Claim ID

          institution_amount: Institution amount in cents

          institution_id: Institution ID

          insurance_id: Insurance ID. Insurance payment is grouped by insurance.

          order_id: Order ID

          patient_amount: Patient amount in cents

          patient_id: Patient ID

          unallocated_amount: Unallocated amount in cents

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/ledger/new-order",
            body=maybe_transform(
                {
                    "claim_amount": claim_amount,
                    "claim_id": claim_id,
                    "institution_amount": institution_amount,
                    "institution_id": institution_id,
                    "insurance_id": insurance_id,
                    "order_id": order_id,
                    "patient_amount": patient_amount,
                    "patient_id": patient_id,
                    "unallocated_amount": unallocated_amount,
                },
                ledger_create_order_params.LedgerCreateOrderParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncLedgerResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLedgerResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLedgerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLedgerResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return AsyncLedgerResourceWithStreamingResponse(self)

    async def create_order(
        self,
        *,
        claim_amount: str,
        claim_id: str,
        institution_amount: str,
        institution_id: str,
        insurance_id: str,
        order_id: str,
        patient_amount: str,
        patient_id: str,
        unallocated_amount: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Args:
          claim_amount: Claim amount in cents

          claim_id: Claim ID

          institution_amount: Institution amount in cents

          institution_id: Institution ID

          insurance_id: Insurance ID. Insurance payment is grouped by insurance.

          order_id: Order ID

          patient_amount: Patient amount in cents

          patient_id: Patient ID

          unallocated_amount: Unallocated amount in cents

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/ledger/new-order",
            body=await async_maybe_transform(
                {
                    "claim_amount": claim_amount,
                    "claim_id": claim_id,
                    "institution_amount": institution_amount,
                    "institution_id": institution_id,
                    "insurance_id": insurance_id,
                    "order_id": order_id,
                    "patient_amount": patient_amount,
                    "patient_id": patient_id,
                    "unallocated_amount": unallocated_amount,
                },
                ledger_create_order_params.LedgerCreateOrderParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class LedgerResourceWithRawResponse:
    def __init__(self, ledger: LedgerResource) -> None:
        self._ledger = ledger

        self.create_order = to_raw_response_wrapper(
            ledger.create_order,
        )


class AsyncLedgerResourceWithRawResponse:
    def __init__(self, ledger: AsyncLedgerResource) -> None:
        self._ledger = ledger

        self.create_order = async_to_raw_response_wrapper(
            ledger.create_order,
        )


class LedgerResourceWithStreamingResponse:
    def __init__(self, ledger: LedgerResource) -> None:
        self._ledger = ledger

        self.create_order = to_streamed_response_wrapper(
            ledger.create_order,
        )


class AsyncLedgerResourceWithStreamingResponse:
    def __init__(self, ledger: AsyncLedgerResource) -> None:
        self._ledger = ledger

        self.create_order = async_to_streamed_response_wrapper(
            ledger.create_order,
        )
