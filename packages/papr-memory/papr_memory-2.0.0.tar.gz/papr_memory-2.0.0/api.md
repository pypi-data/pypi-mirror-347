# User

Types:

```python
from papr.types import UserResponse, UserType, UserListResponse, UserDeleteResponse
```

Methods:

- <code title="post /v1/user">client.user.<a href="./src/papr/resources/user.py">create</a>(\*\*<a href="src/papr/types/user_create_params.py">params</a>) -> <a href="./src/papr/types/user_response.py">UserResponse</a></code>
- <code title="put /v1/user/{user_id}">client.user.<a href="./src/papr/resources/user.py">update</a>(user_id, \*\*<a href="src/papr/types/user_update_params.py">params</a>) -> <a href="./src/papr/types/user_response.py">UserResponse</a></code>
- <code title="get /v1/user">client.user.<a href="./src/papr/resources/user.py">list</a>(\*\*<a href="src/papr/types/user_list_params.py">params</a>) -> <a href="./src/papr/types/user_list_response.py">UserListResponse</a></code>
- <code title="delete /v1/user/{user_id}">client.user.<a href="./src/papr/resources/user.py">delete</a>(user_id) -> <a href="./src/papr/types/user_delete_response.py">UserDeleteResponse</a></code>
- <code title="get /v1/user/{user_id}">client.user.<a href="./src/papr/resources/user.py">get</a>(user_id) -> <a href="./src/papr/types/user_response.py">UserResponse</a></code>

# Memory

Types:

```python
from papr.types import (
    AddMemory,
    AddMemoryResponse,
    ContextItem,
    MemoryMetadata,
    MemoryType,
    RelationshipItem,
    SearchResponse,
    MemoryUpdateResponse,
    MemoryDeleteResponse,
    MemoryAddBatchResponse,
)
```

Methods:

- <code title="put /v1/memory/{memory_id}">client.memory.<a href="./src/papr/resources/memory.py">update</a>(memory_id, \*\*<a href="src/papr/types/memory_update_params.py">params</a>) -> <a href="./src/papr/types/memory_update_response.py">MemoryUpdateResponse</a></code>
- <code title="delete /v1/memory/{memory_id}">client.memory.<a href="./src/papr/resources/memory.py">delete</a>(memory_id, \*\*<a href="src/papr/types/memory_delete_params.py">params</a>) -> <a href="./src/papr/types/memory_delete_response.py">MemoryDeleteResponse</a></code>
- <code title="post /v1/memory">client.memory.<a href="./src/papr/resources/memory.py">add</a>(\*\*<a href="src/papr/types/memory_add_params.py">params</a>) -> <a href="./src/papr/types/add_memory_response.py">AddMemoryResponse</a></code>
- <code title="post /v1/memory/batch">client.memory.<a href="./src/papr/resources/memory.py">add_batch</a>(\*\*<a href="src/papr/types/memory_add_batch_params.py">params</a>) -> <a href="./src/papr/types/memory_add_batch_response.py">MemoryAddBatchResponse</a></code>
- <code title="get /v1/memory/{memory_id}">client.memory.<a href="./src/papr/resources/memory.py">get</a>(memory_id) -> <a href="./src/papr/types/search_response.py">SearchResponse</a></code>

# Document

Types:

```python
from papr.types import AddMemoryItem, DocumentUploadResponse
```

Methods:

- <code title="post /v1/document">client.document.<a href="./src/papr/resources/document.py">upload</a>(\*\*<a href="src/papr/types/document_upload_params.py">params</a>) -> <a href="./src/papr/types/document_upload_response.py">DocumentUploadResponse</a></code>

# Search

Methods:

- <code title="post /v1/search">client.search.<a href="./src/papr/resources/search.py">perform</a>(\*\*<a href="src/papr/types/search_perform_params.py">params</a>) -> <a href="./src/papr/types/search_response.py">SearchResponse</a></code>
