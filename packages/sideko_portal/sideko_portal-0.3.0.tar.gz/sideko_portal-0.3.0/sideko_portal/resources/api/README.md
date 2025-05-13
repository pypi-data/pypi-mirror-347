
### Delete an API <a name="delete"></a>



**API Endpoint**: `DELETE /api/{api_name}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.delete(api_name="my-project")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.delete(api_name="my-project")
```

### List your APIs <a name="list"></a>



**API Endpoint**: `GET /api`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.list()
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.list()
```

### Get one API <a name="get"></a>



**API Endpoint**: `GET /api/{api_name}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.get(api_name="my-project")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.get(api_name="my-project")
```

### Update an existing API <a name="patch"></a>



**API Endpoint**: `PATCH /api/{api_name}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.patch(api_name="my-project", name="my-new-api-name")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.patch(api_name="my-project", name="my-new-api-name")
```

### Create a new API <a name="create"></a>



**API Endpoint**: `POST /api`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.create(name="my-api-spec")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.create(name="my-api-spec")
```

### Create an API with an initial version <a name="init"></a>



**API Endpoint**: `POST /api/init`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.init(
    name="my-api-spec",
    openapi=open("uploads/openapi.yaml", "rb"),
    version="major",
    notes="<p>This version includes a number of excellent improvements</p>",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.init(
    name="my-api-spec",
    openapi=open("uploads/openapi.yaml", "rb"),
    version="major",
    notes="<p>This version includes a number of excellent improvements</p>",
)
```
