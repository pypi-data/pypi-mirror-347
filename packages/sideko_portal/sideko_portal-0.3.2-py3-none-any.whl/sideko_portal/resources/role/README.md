
### Delete role and all associated permissions <a name="delete"></a>



**API Endpoint**: `DELETE /role/{id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.role.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.role.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

### List roles <a name="list"></a>



**API Endpoint**: `GET /role`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.role.list()
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.role.list()
```

### Create a new role <a name="create"></a>



**API Endpoint**: `POST /role`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.role.create(
    object_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    object_type="api_project",
    role_definition_id="ApiProjectAdmin",
    user_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.role.create(
    object_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    object_type="api_project",
    role_definition_id="ApiProjectAdmin",
    user_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
)
```
