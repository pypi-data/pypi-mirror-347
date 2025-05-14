
### Removes an API link <a name="delete"></a>



**API Endpoint**: `DELETE /api_link/{id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api_link.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api_link.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

### List API links for doc version <a name="list"></a>



**API Endpoint**: `GET /api_link`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api_link.list(
    doc_name="my-project", doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api_link.list(
    doc_name="my-project", doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"
)
```

### Retrieve single API link <a name="get"></a>



**API Endpoint**: `GET /api_link/{id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api_link.get(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api_link.get(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

### Updates an API link <a name="patch"></a>



**API Endpoint**: `PATCH /api_link/{id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api_link.patch(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api_link.patch(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

### Links API Version to Documentation project version with a specified update policy <a name="create"></a>



**API Endpoint**: `POST /api_link`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api_link.create(
    doc_version_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    group_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    nav_label="string",
    policy={"api_id": "my-api", "type_": "latest"},
    slug="string",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api_link.create(
    doc_version_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    group_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    nav_label="string",
    policy={"api_id": "my-api", "type_": "latest"},
    slug="string",
)
```

### Reorder API links and groups <a name="reorder"></a>



**API Endpoint**: `POST /api_link/reorder`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api_link.reorder(
    doc_version_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    groups=[{"id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a", "order": 123}],
    links=[
        {
            "group_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            "id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            "order": 123,
        }
    ],
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api_link.reorder(
    doc_version_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    groups=[{"id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a", "order": 123}],
    links=[
        {
            "group_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            "id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            "order": 123,
        }
    ],
)
```
