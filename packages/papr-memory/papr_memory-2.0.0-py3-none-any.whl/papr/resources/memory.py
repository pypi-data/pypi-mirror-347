# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional

import httpx

from ..types import (
    MemoryType,
    memory_add_params,
    memory_delete_params,
    memory_update_params,
    memory_add_batch_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.memory_type import MemoryType
from ..types.search_response import SearchResponse
from ..types.add_memory_param import AddMemoryParam
from ..types.context_item_param import ContextItemParam
from ..types.add_memory_response import AddMemoryResponse
from ..types.memory_metadata_param import MemoryMetadataParam
from ..types.memory_delete_response import MemoryDeleteResponse
from ..types.memory_update_response import MemoryUpdateResponse
from ..types.relationship_item_param import RelationshipItemParam
from ..types.memory_add_batch_response import MemoryAddBatchResponse

__all__ = ["MemoryResource", "AsyncMemoryResource"]


class MemoryResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MemoryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Papr-ai/Python-SDK#accessing-raw-response-data-eg-headers
        """
        return MemoryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MemoryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Papr-ai/Python-SDK#with_streaming_response
        """
        return MemoryResourceWithStreamingResponse(self)

    def update(
        self,
        memory_id: str,
        *,
        content: Optional[str] | NotGiven = NOT_GIVEN,
        context: Optional[Iterable[ContextItemParam]] | NotGiven = NOT_GIVEN,
        metadata: Optional[MemoryMetadataParam] | NotGiven = NOT_GIVEN,
        relationships_json: Optional[Iterable[RelationshipItemParam]] | NotGiven = NOT_GIVEN,
        type: Optional[MemoryType] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MemoryUpdateResponse:
        """
        Update an existing memory item by ID.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Required Headers**:
            - Content-Type: application/json
            - X-Client-Type: (e.g., 'papr_plugin', 'browser_extension')

            The API validates content size against MAX_CONTENT_LENGTH environment variable (defaults to 15000 bytes).

        Args:
          content: The new content of the memory item

          context: Updated context for the memory item

          metadata: Metadata for memory request

          relationships_json: Updated relationships for Graph DB (neo4J)

          type: Valid memory types

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return self._put(
            f"/v1/memory/{memory_id}",
            body=maybe_transform(
                {
                    "content": content,
                    "context": context,
                    "metadata": metadata,
                    "relationships_json": relationships_json,
                    "type": type,
                },
                memory_update_params.MemoryUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryUpdateResponse,
        )

    def delete(
        self,
        memory_id: str,
        *,
        skip_parse: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MemoryDeleteResponse:
        """
        Delete a memory item by ID.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Required Headers**:
            - X-Client-Type: (e.g., 'papr_plugin', 'browser_extension')

        Args:
          skip_parse: Skip Parse Server deletion

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return self._delete(
            f"/v1/memory/{memory_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"skip_parse": skip_parse}, memory_delete_params.MemoryDeleteParams),
            ),
            cast_to=MemoryDeleteResponse,
        )

    def add(
        self,
        *,
        content: str,
        skip_background_processing: bool | NotGiven = NOT_GIVEN,
        context: Optional[Iterable[ContextItemParam]] | NotGiven = NOT_GIVEN,
        metadata: Optional[MemoryMetadataParam] | NotGiven = NOT_GIVEN,
        relationships_json: Optional[Iterable[RelationshipItemParam]] | NotGiven = NOT_GIVEN,
        type: MemoryType | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddMemoryResponse:
        """
        Add a new memory item to the system with size validation and background
        processing.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Required Headers**:
            - Content-Type: application/json
            - X-Client-Type: (e.g., 'papr_plugin', 'browser_extension')

            The API validates content size against MAX_CONTENT_LENGTH environment variable (defaults to 15000 bytes).

        Args:
          content: The content of the memory item you want to add to memory

          skip_background_processing: If True, skips adding background tasks for processing

          context: Context can be conversation history or any relevant context for a memory item

          metadata: Metadata for memory request

          relationships_json: Array of relationships that we can use in Graph DB (neo4J)

          type: Content type of the memory item

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/memory",
            body=maybe_transform(
                {
                    "content": content,
                    "context": context,
                    "metadata": metadata,
                    "relationships_json": relationships_json,
                    "type": type,
                },
                memory_add_params.MemoryAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"skip_background_processing": skip_background_processing}, memory_add_params.MemoryAddParams
                ),
            ),
            cast_to=AddMemoryResponse,
        )

    def add_batch(
        self,
        *,
        memories: Iterable[AddMemoryParam],
        skip_background_processing: bool | NotGiven = NOT_GIVEN,
        batch_size: Optional[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MemoryAddBatchResponse:
        """
        Add multiple memory items in a batch with size validation and background
        processing.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Required Headers**:
            - Content-Type: application/json
            - X-Client-Type: (e.g., 'papr_plugin', 'browser_extension')

            The API validates individual memory content size against MAX_CONTENT_LENGTH environment variable (defaults to 15000 bytes).

        Args:
          memories: List of memory items to add in batch

          skip_background_processing: If True, skips adding background tasks for processing

          batch_size: Number of items to process in parallel

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/memory/batch",
            body=maybe_transform(
                {
                    "memories": memories,
                    "batch_size": batch_size,
                },
                memory_add_batch_params.MemoryAddBatchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"skip_background_processing": skip_background_processing},
                    memory_add_batch_params.MemoryAddBatchParams,
                ),
            ),
            cast_to=MemoryAddBatchResponse,
        )

    def get(
        self,
        memory_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchResponse:
        """
        Retrieve a memory item by ID.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Required Headers**:
            - X-Client-Type: (e.g., 'papr_plugin', 'browser_extension')

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return self._get(
            f"/v1/memory/{memory_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchResponse,
        )


class AsyncMemoryResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMemoryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Papr-ai/Python-SDK#accessing-raw-response-data-eg-headers
        """
        return AsyncMemoryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMemoryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Papr-ai/Python-SDK#with_streaming_response
        """
        return AsyncMemoryResourceWithStreamingResponse(self)

    async def update(
        self,
        memory_id: str,
        *,
        content: Optional[str] | NotGiven = NOT_GIVEN,
        context: Optional[Iterable[ContextItemParam]] | NotGiven = NOT_GIVEN,
        metadata: Optional[MemoryMetadataParam] | NotGiven = NOT_GIVEN,
        relationships_json: Optional[Iterable[RelationshipItemParam]] | NotGiven = NOT_GIVEN,
        type: Optional[MemoryType] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MemoryUpdateResponse:
        """
        Update an existing memory item by ID.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Required Headers**:
            - Content-Type: application/json
            - X-Client-Type: (e.g., 'papr_plugin', 'browser_extension')

            The API validates content size against MAX_CONTENT_LENGTH environment variable (defaults to 15000 bytes).

        Args:
          content: The new content of the memory item

          context: Updated context for the memory item

          metadata: Metadata for memory request

          relationships_json: Updated relationships for Graph DB (neo4J)

          type: Valid memory types

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return await self._put(
            f"/v1/memory/{memory_id}",
            body=await async_maybe_transform(
                {
                    "content": content,
                    "context": context,
                    "metadata": metadata,
                    "relationships_json": relationships_json,
                    "type": type,
                },
                memory_update_params.MemoryUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemoryUpdateResponse,
        )

    async def delete(
        self,
        memory_id: str,
        *,
        skip_parse: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MemoryDeleteResponse:
        """
        Delete a memory item by ID.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Required Headers**:
            - X-Client-Type: (e.g., 'papr_plugin', 'browser_extension')

        Args:
          skip_parse: Skip Parse Server deletion

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return await self._delete(
            f"/v1/memory/{memory_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"skip_parse": skip_parse}, memory_delete_params.MemoryDeleteParams),
            ),
            cast_to=MemoryDeleteResponse,
        )

    async def add(
        self,
        *,
        content: str,
        skip_background_processing: bool | NotGiven = NOT_GIVEN,
        context: Optional[Iterable[ContextItemParam]] | NotGiven = NOT_GIVEN,
        metadata: Optional[MemoryMetadataParam] | NotGiven = NOT_GIVEN,
        relationships_json: Optional[Iterable[RelationshipItemParam]] | NotGiven = NOT_GIVEN,
        type: MemoryType | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddMemoryResponse:
        """
        Add a new memory item to the system with size validation and background
        processing.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Required Headers**:
            - Content-Type: application/json
            - X-Client-Type: (e.g., 'papr_plugin', 'browser_extension')

            The API validates content size against MAX_CONTENT_LENGTH environment variable (defaults to 15000 bytes).

        Args:
          content: The content of the memory item you want to add to memory

          skip_background_processing: If True, skips adding background tasks for processing

          context: Context can be conversation history or any relevant context for a memory item

          metadata: Metadata for memory request

          relationships_json: Array of relationships that we can use in Graph DB (neo4J)

          type: Content type of the memory item

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/memory",
            body=await async_maybe_transform(
                {
                    "content": content,
                    "context": context,
                    "metadata": metadata,
                    "relationships_json": relationships_json,
                    "type": type,
                },
                memory_add_params.MemoryAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"skip_background_processing": skip_background_processing}, memory_add_params.MemoryAddParams
                ),
            ),
            cast_to=AddMemoryResponse,
        )

    async def add_batch(
        self,
        *,
        memories: Iterable[AddMemoryParam],
        skip_background_processing: bool | NotGiven = NOT_GIVEN,
        batch_size: Optional[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MemoryAddBatchResponse:
        """
        Add multiple memory items in a batch with size validation and background
        processing.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Required Headers**:
            - Content-Type: application/json
            - X-Client-Type: (e.g., 'papr_plugin', 'browser_extension')

            The API validates individual memory content size against MAX_CONTENT_LENGTH environment variable (defaults to 15000 bytes).

        Args:
          memories: List of memory items to add in batch

          skip_background_processing: If True, skips adding background tasks for processing

          batch_size: Number of items to process in parallel

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/memory/batch",
            body=await async_maybe_transform(
                {
                    "memories": memories,
                    "batch_size": batch_size,
                },
                memory_add_batch_params.MemoryAddBatchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"skip_background_processing": skip_background_processing},
                    memory_add_batch_params.MemoryAddBatchParams,
                ),
            ),
            cast_to=MemoryAddBatchResponse,
        )

    async def get(
        self,
        memory_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchResponse:
        """
        Retrieve a memory item by ID.

            **Authentication Required**:
            One of the following authentication methods must be used:
            - Bearer token in `Authorization` header
            - API Key in `X-API-Key` header
            - Session token in `X-Session-Token` header

            **Required Headers**:
            - X-Client-Type: (e.g., 'papr_plugin', 'browser_extension')

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not memory_id:
            raise ValueError(f"Expected a non-empty value for `memory_id` but received {memory_id!r}")
        return await self._get(
            f"/v1/memory/{memory_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchResponse,
        )


class MemoryResourceWithRawResponse:
    def __init__(self, memory: MemoryResource) -> None:
        self._memory = memory

        self.update = to_raw_response_wrapper(
            memory.update,
        )
        self.delete = to_raw_response_wrapper(
            memory.delete,
        )
        self.add = to_raw_response_wrapper(
            memory.add,
        )
        self.add_batch = to_raw_response_wrapper(
            memory.add_batch,
        )
        self.get = to_raw_response_wrapper(
            memory.get,
        )


class AsyncMemoryResourceWithRawResponse:
    def __init__(self, memory: AsyncMemoryResource) -> None:
        self._memory = memory

        self.update = async_to_raw_response_wrapper(
            memory.update,
        )
        self.delete = async_to_raw_response_wrapper(
            memory.delete,
        )
        self.add = async_to_raw_response_wrapper(
            memory.add,
        )
        self.add_batch = async_to_raw_response_wrapper(
            memory.add_batch,
        )
        self.get = async_to_raw_response_wrapper(
            memory.get,
        )


class MemoryResourceWithStreamingResponse:
    def __init__(self, memory: MemoryResource) -> None:
        self._memory = memory

        self.update = to_streamed_response_wrapper(
            memory.update,
        )
        self.delete = to_streamed_response_wrapper(
            memory.delete,
        )
        self.add = to_streamed_response_wrapper(
            memory.add,
        )
        self.add_batch = to_streamed_response_wrapper(
            memory.add_batch,
        )
        self.get = to_streamed_response_wrapper(
            memory.get,
        )


class AsyncMemoryResourceWithStreamingResponse:
    def __init__(self, memory: AsyncMemoryResource) -> None:
        self._memory = memory

        self.update = async_to_streamed_response_wrapper(
            memory.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            memory.delete,
        )
        self.add = async_to_streamed_response_wrapper(
            memory.add,
        )
        self.add_batch = async_to_streamed_response_wrapper(
            memory.add_batch,
        )
        self.get = async_to_streamed_response_wrapper(
            memory.get,
        )
