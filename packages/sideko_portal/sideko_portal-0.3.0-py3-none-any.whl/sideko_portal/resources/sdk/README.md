
### List all managed SDKs <a name="list"></a>



**API Endpoint**: `GET /sdk`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.sdk.list()
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.sdk.list()
```

### Generate a new managed SDK from a Sideko configuration file <a name="generate"></a>



**API Endpoint**: `POST /sdk`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.sdk.generate(
    config=open("uploads/config.yaml", "rb"), language="go", sdk_version="0.1.0"
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.sdk.generate(
    config=open("uploads/config.yaml", "rb"), language="go", sdk_version="0.1.0"
)
```

### Update an SDK to reflect the latest state of the API <a name="update"></a>



**API Endpoint**: `POST /sdk/update`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.sdk.update(
    config=open("uploads/config.yaml", "rb"),
    prev_sdk_git=open("uploads/git.tar.gz", "rb"),
    prev_sdk_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    sdk_version="major",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.sdk.update(
    config=open("uploads/config.yaml", "rb"),
    prev_sdk_git=open("uploads/git.tar.gz", "rb"),
    prev_sdk_id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a",
    sdk_version="major",
)
```
