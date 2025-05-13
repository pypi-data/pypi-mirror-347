
### List deployments for a specific documentation project <a name="list"></a>

Retrieves all deployments for a doc project

**API Endpoint**: `GET /doc_project/{doc_name}/deployment`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.deployment.list(doc_name="my-project")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.deployment.list(doc_name="my-project")
```

### Get a specific deployment for a specific documentation project <a name="get"></a>

Retrieves single deployment

**API Endpoint**: `GET /doc_project/{doc_name}/deployment/{deployment_id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.deployment.get(
    deployment_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a", doc_name="my-project"
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.deployment.get(
    deployment_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a", doc_name="my-project"
)
```

### Deploy a new generated version of documentation with linked guides & APIs <a name="trigger"></a>

Deploys a new generated version of documentation with linked guides & APIs

**API Endpoint**: `POST /doc_project/{doc_name}/deployment`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.deployment.trigger(doc_name="my-project", target="Preview")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.deployment.trigger(doc_name="my-project", target="Preview")
```
