# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import search_perform_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, strip_not_given, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.search_response import SearchResponse

__all__ = ["SearchResource", "AsyncSearchResource"]


class SearchResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Papr-ai/Python-SDK#accessing-raw-response-data-eg-headers
        """
        return SearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Papr-ai/Python-SDK#with_streaming_response
        """
        return SearchResourceWithStreamingResponse(self)

    def perform(
        self,
        *,
        query: str,
        max_memories: int | NotGiven = NOT_GIVEN,
        max_nodes: int | NotGiven = NOT_GIVEN,
        rank_results: bool | NotGiven = NOT_GIVEN,
        accept_encoding: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchResponse:
        """
        Search through memories with authentication required.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Recommended Headers**:
            ```
            Accept-Encoding: gzip
            ```

            The API supports response compression for improved performance. Responses larger than 1KB will be automatically compressed when this header is present.

        Args:
          query: Detailed search query describing what you're looking for. For best results,
              write 2-3 sentences that include specific details, context, and time frame. For
              example: 'Find recurring customer complaints about API performance from the last
              month. Focus on issues where customers specifically mentioned timeout errors or
              slow response times in their conversations.'

          max_memories: Maximum number of memories to return

          max_nodes: Maximum number of neo nodes to return

          rank_results: Whether to enable additional ranking of search results. Default is false because
              results are already ranked when using an LLM for search (recommended approach).
              Only enable this if you're not using an LLM in your search pipeline and need
              additional result ranking.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"Accept-Encoding": accept_encoding}), **(extra_headers or {})}
        return self._post(
            "/v1/search",
            body=maybe_transform(
                {
                    "query": query,
                    "rank_results": rank_results,
                },
                search_perform_params.SearchPerformParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "max_memories": max_memories,
                        "max_nodes": max_nodes,
                    },
                    search_perform_params.SearchPerformParams,
                ),
            ),
            cast_to=SearchResponse,
        )


class AsyncSearchResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Papr-ai/Python-SDK#accessing-raw-response-data-eg-headers
        """
        return AsyncSearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Papr-ai/Python-SDK#with_streaming_response
        """
        return AsyncSearchResourceWithStreamingResponse(self)

    async def perform(
        self,
        *,
        query: str,
        max_memories: int | NotGiven = NOT_GIVEN,
        max_nodes: int | NotGiven = NOT_GIVEN,
        rank_results: bool | NotGiven = NOT_GIVEN,
        accept_encoding: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchResponse:
        """
        Search through memories with authentication required.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Recommended Headers**:
            ```
            Accept-Encoding: gzip
            ```

            The API supports response compression for improved performance. Responses larger than 1KB will be automatically compressed when this header is present.

        Args:
          query: Detailed search query describing what you're looking for. For best results,
              write 2-3 sentences that include specific details, context, and time frame. For
              example: 'Find recurring customer complaints about API performance from the last
              month. Focus on issues where customers specifically mentioned timeout errors or
              slow response times in their conversations.'

          max_memories: Maximum number of memories to return

          max_nodes: Maximum number of neo nodes to return

          rank_results: Whether to enable additional ranking of search results. Default is false because
              results are already ranked when using an LLM for search (recommended approach).
              Only enable this if you're not using an LLM in your search pipeline and need
              additional result ranking.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"Accept-Encoding": accept_encoding}), **(extra_headers or {})}
        return await self._post(
            "/v1/search",
            body=await async_maybe_transform(
                {
                    "query": query,
                    "rank_results": rank_results,
                },
                search_perform_params.SearchPerformParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "max_memories": max_memories,
                        "max_nodes": max_nodes,
                    },
                    search_perform_params.SearchPerformParams,
                ),
            ),
            cast_to=SearchResponse,
        )


class SearchResourceWithRawResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.perform = to_raw_response_wrapper(
            search.perform,
        )


class AsyncSearchResourceWithRawResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.perform = async_to_raw_response_wrapper(
            search.perform,
        )


class SearchResourceWithStreamingResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.perform = to_streamed_response_wrapper(
            search.perform,
        )


class AsyncSearchResourceWithStreamingResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.perform = async_to_streamed_response_wrapper(
            search.perform,
        )
