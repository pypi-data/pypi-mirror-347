
### Initialize an SDK configuration with all defaults applied <a name="init"></a>

Creates a sdk config with default configurations for the api/api version

**API Endpoint**: `POST /sdk/config/init`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.sdk.config.init(api_name="my-project")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.sdk.config.init(api_name="my-project")
```

### Sync an SDK configuration with the latest state of the API <a name="sync"></a>

Updates provided config with missing default configurations for the api version

**API Endpoint**: `POST /sdk/config/sync`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.sdk.config.sync(
    config=open("uploads/config.yaml", "rb"), openapi=open("uploads/openapi.yaml", "rb")
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.sdk.config.sync(
    config=open("uploads/config.yaml", "rb"), openapi=open("uploads/openapi.yaml", "rb")
)
```
