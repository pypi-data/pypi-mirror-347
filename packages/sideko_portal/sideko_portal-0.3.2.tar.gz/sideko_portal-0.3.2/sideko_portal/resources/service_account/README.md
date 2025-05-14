
### Delete a service account <a name="delete"></a>



**API Endpoint**: `DELETE /service_account/{id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.service_account.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.service_account.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

### List all service accounts in organization <a name="list"></a>



**API Endpoint**: `GET /service_account`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.service_account.list()
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.service_account.list()
```

### Get service account by the ID <a name="get"></a>



**API Endpoint**: `GET /service_account/{id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.service_account.get(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.service_account.get(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

### Create a new service account with a set of project permissions <a name="create"></a>



**API Endpoint**: `POST /service_account`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.service_account.create(
    name="Documentation Publisher Service Account",
    object_roles=[
        {
            "object_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            "object_type": "api_project",
            "role_definition_id": "ApiProjectAdmin",
        }
    ],
    expiration="2025-01-01T00:00:00",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.service_account.create(
    name="Documentation Publisher Service Account",
    object_roles=[
        {
            "object_id": "3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
            "object_type": "api_project",
            "role_definition_id": "ApiProjectAdmin",
        }
    ],
    expiration="2025-01-01T00:00:00",
)
```
