
### Get the theme attached to a documentation project <a name="get"></a>



**API Endpoint**: `GET /doc_project/{doc_name}/theme`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.theme.get(doc_name="my-project")
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.theme.get(doc_name="my-project")
```

### Update a document project theme <a name="update"></a>



**API Endpoint**: `PUT /doc_project/{doc_name}/theme`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.doc.theme.update(
    doc_name="my-project",
    api_reference_group_variant="grouped",
    dark_active_button_bg_color="#FFFFFF",
    dark_active_button_text_color="#FFFFFF",
    dark_bg_color="#FFFFFF",
    dark_navbar_color="#FFFFFF",
    dark_navbar_text_color="#FFFFFF",
    light_active_button_bg_color="#FFFFFF",
    light_active_button_text_color="#FFFFFF",
    light_bg_color="#FFFFFF",
    light_navbar_color="#FFFFFF",
    light_navbar_text_color="#FFFFFF",
)
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.doc.theme.update(
    doc_name="my-project",
    api_reference_group_variant="grouped",
    dark_active_button_bg_color="#FFFFFF",
    dark_active_button_text_color="#FFFFFF",
    dark_bg_color="#FFFFFF",
    dark_navbar_color="#FFFFFF",
    dark_navbar_text_color="#FFFFFF",
    light_active_button_bg_color="#FFFFFF",
    light_active_button_text_color="#FFFFFF",
    light_bg_color="#FFFFFF",
    light_navbar_color="#FFFFFF",
    light_navbar_text_color="#FFFFFF",
)
```
