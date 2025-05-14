
### Retrieve SDK documentation <a name="create"></a>

Get documentation for a specific SDK

**API Endpoint**: `POST /sdk/{sdk_id}/doc`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.sdk.doc.create(sdk_id="h1jasdf123", modules_filter=["user.admin"])
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.sdk.doc.create(sdk_id="h1jasdf123", modules_filter=["user.admin"])
```
