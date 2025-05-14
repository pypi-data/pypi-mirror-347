
### Delete Asset <a name="delete"></a>

Delete a media asset in your organization

**API Endpoint**: `DELETE /organization/asset/{id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.asset.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.asset.delete(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

### List Assets <a name="list"></a>

Get all media assets for an organization

**API Endpoint**: `GET /organization/asset`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.asset.list()
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.asset.list()
```

### Update Asset <a name="patch"></a>

Update a media asset in your organization

**API Endpoint**: `PATCH /organization/asset/{id}`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.asset.patch(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.asset.patch(id="3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a")
```

### Upload Assets <a name="create"></a>

Add a media asset like logos or other media to an organization

**API Endpoint**: `POST /organization/asset`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.asset.create(file=open("uploads/image.png", "rb"))
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.asset.create(file=open("uploads/image.png", "rb"))
```
