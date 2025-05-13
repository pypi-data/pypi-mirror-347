
### Delete an API Specification and it's associated metadata <a name="delete"></a>



**API Endpoint**: `DELETE /api/{api_name}/spec/{api_version}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.spec.delete(api_name="my-project", api_version="latest")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.spec.delete(api_name="my-project", api_version="latest")
```

### List specs of a collection <a name="list"></a>



**API Endpoint**: `GET /api/{api_name}/spec`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.spec.list(api_name="my-project")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.spec.list(api_name="my-project")
```

### Get API specification metadata <a name="get"></a>



**API Endpoint**: `GET /api/{api_name}/spec/{api_version}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.spec.get(api_name="my-project", api_version="latest")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.spec.get(api_name="my-project", api_version="latest")
```

### Get OpenAPI specification <a name="get_openapi"></a>



**API Endpoint**: `GET /api/{api_name}/spec/{api_version}/openapi`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.spec.get_openapi(api_name="my-project", api_version="latest")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.spec.get_openapi(api_name="my-project", api_version="latest")
```

### Get Stats about the specification <a name="get_stats"></a>



**API Endpoint**: `GET /api/{api_name}/spec/{api_version}/stats`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.spec.get_stats(api_name="my-project", api_version="latest")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.spec.get_stats(api_name="my-project", api_version="latest")
```

### Update an API Specification and/or metadata <a name="patch"></a>



**API Endpoint**: `PATCH /api/{api_name}/spec/{api_version}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.spec.patch(
    api_name="my-project",
    api_version="latest",
    notes="<p>This version includes a number of excellent improvements</p>",
    openapi=open("uploads/openapi.yaml", "rb"),
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.api.spec.patch(
    api_name="my-project",
    api_version="latest",
    notes="<p>This version includes a number of excellent improvements</p>",
    openapi=open("uploads/openapi.yaml", "rb"),
)
```

### Add a new API specification <a name="create"></a>



**API Endpoint**: `POST /api/{api_name}/spec`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.api.spec.create(
    api_name="my-project",
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
res = await client.api.spec.create(
    api_name="my-project",
    openapi=open("uploads/openapi.yaml", "rb"),
    version="major",
    notes="<p>This version includes a number of excellent improvements</p>",
)
```
