
### Delete a specific guide for a specific version of a documentation project <a name="delete"></a>



**API Endpoint**: `DELETE /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.version.guide.delete(
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.version.guide.delete(
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
)
```

### List guides for a specific version of a documentation project <a name="list"></a>



**API Endpoint**: `GET /doc_project/{doc_name}/version/{doc_version}/guide`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.version.guide.list(
    doc_name="my-project", doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.version.guide.list(
    doc_name="my-project", doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"
)
```

### Get a specific guide for a specific version of a documentation project <a name="get"></a>



**API Endpoint**: `GET /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.version.guide.get(
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.version.guide.get(
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
)
```

### Get content for a specific guide for a specific version of a documentation project <a name="get_content"></a>



**API Endpoint**: `GET /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}/content`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.version.guide.get_content(
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.version.guide.get_content(
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
)
```

### Update a specific guide for a specific version of a documentation project <a name="patch"></a>



**API Endpoint**: `PATCH /doc_project/{doc_name}/version/{doc_version}/guide/{guide_id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.version.guide.patch(
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    icon="house",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.version.guide.patch(
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    guide_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    icon="house",
)
```

### Create a guide for a specific version of a documentation project <a name="create"></a>



**API Endpoint**: `POST /doc_project/{doc_name}/version/{doc_version}/guide`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.version.guide.create(
    content="string",
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    is_parent=True,
    nav_label="string",
    slug="string",
    icon="house",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.version.guide.create(
    content="string",
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    is_parent=True,
    nav_label="string",
    slug="string",
    icon="house",
)
```

### Reorder guides for a specific version of a documentation project <a name="reorder"></a>



**API Endpoint**: `POST /doc_project/{doc_name}/version/{doc_version}/guide/reorder`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.version.guide.reorder(
    data=[
        {
            "id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            "order": 123,
            "parent_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        }
    ],
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.version.guide.reorder(
    data=[
        {
            "id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            "order": 123,
            "parent_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
        }
    ],
    doc_name="my-project",
    doc_version="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
)
```
