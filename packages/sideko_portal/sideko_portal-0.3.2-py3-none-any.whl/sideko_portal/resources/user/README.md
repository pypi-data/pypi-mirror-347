
### Invite a user to an organization with a specific role <a name="invite"></a>



**API Endpoint**: `POST /user/invite`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.user.invite(email="user@example.com", role_definition_id="ApiProjectAdmin")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.user.invite(
    email="user@example.com", role_definition_id="ApiProjectAdmin"
)
```
