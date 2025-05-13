
### Delete a specific Documentation Project <a name="delete"></a>



**API Endpoint**: `DELETE /doc_project/{doc_name}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.delete(doc_name="my-project")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.delete(doc_name="my-project")
```

### List Documentation Projects <a name="list"></a>



**API Endpoint**: `GET /doc_project`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.list()
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.list()
```

### Get a specific Documentation Project <a name="get"></a>



**API Endpoint**: `GET /doc_project/{doc_name}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.get(doc_name="my-project")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.get(doc_name="my-project")
```

### A simple check to see if the requesting user has access to the preview doc project <a name="check_preview"></a>



**API Endpoint**: `GET /doc_project/{doc_name}/preview`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.check_preview(
    doc_name="my-project", pathname="%2Freferences%my-api%2Fmy-get-documentation"
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.check_preview(
    doc_name="my-project", pathname="%2Freferences%my-api%2Fmy-get-documentation"
)
```

### Update an existing Documentation Project <a name="patch"></a>



**API Endpoint**: `PATCH /doc_project/{doc_name}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.patch(doc_name="my-project", name="my-company-docs")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.patch(doc_name="my-project", name="my-company-docs")
```

### Create a new Documentation Project <a name="create"></a>



**API Endpoint**: `POST /doc_project`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.create(name="my-company-docs")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.create(name="my-company-docs")
```
