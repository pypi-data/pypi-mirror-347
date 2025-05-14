
### Lint an OpenAPI spec <a name="run"></a>



**API Endpoint**: `POST /lint`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.lint.run(api_name="my-project", openapi=open("uploads/openapi.yaml", "rb"))
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.lint.run(
    api_name="my-project", openapi=open("uploads/openapi.yaml", "rb")
)
```
