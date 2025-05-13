
### Deletes a preview environment password <a name="delete_password"></a>



**API Endpoint**: `DELETE /doc_project/{doc_name}/password`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.preview.delete_password(
    doc_name="my-project", name="My customer preview"
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.preview.delete_password(
    doc_name="my-project", name="My customer preview"
)
```

### Lists generated passwords for a documentation project preview environment <a name="list_passwords"></a>



**API Endpoint**: `GET /doc_project/{doc_name}/password`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.preview.list_passwords(doc_name="my-project")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.preview.list_passwords(doc_name="my-project")
```

### A password generator for a documentation project preview environment <a name="create_password"></a>



**API Endpoint**: `POST /doc_project/{doc_name}/password`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.preview.create_password(
    doc_name="my-project", name="My customer preview"
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.preview.create_password(
    doc_name="my-project", name="My customer preview"
)
```
