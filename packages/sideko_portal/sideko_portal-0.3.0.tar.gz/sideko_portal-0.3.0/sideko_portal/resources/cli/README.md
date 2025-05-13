
### Checks if current CLI has updates <a name="check_updates"></a>



**API Endpoint**: `GET /cli/updates/{cli_version}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.cli.check_updates(cli_version="0.1.0")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.cli.check_updates(cli_version="0.1.0")
```
