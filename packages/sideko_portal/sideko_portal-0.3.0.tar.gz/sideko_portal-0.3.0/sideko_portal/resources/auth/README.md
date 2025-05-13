
### Exchange one-time auth key for api key <a name="exchange_code"></a>



**API Endpoint**: `GET /auth/exchange_key`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.auth.exchange_code(code="string")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.auth.exchange_code(code="string")
```
