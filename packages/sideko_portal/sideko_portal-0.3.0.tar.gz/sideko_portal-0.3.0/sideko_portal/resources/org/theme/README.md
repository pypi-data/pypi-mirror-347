
### Get organization theme <a name="get"></a>

Retrieves the documentation project theme configured at the organization level

**API Endpoint**: `GET /organization/theme`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.org.theme.get()
```

#### Asynchronous Client

```python
from os import getenv
from sideko_portal import AsyncSidekoClient

client = AsyncSidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = await client.org.theme.get()
```

### Update organization theme <a name="update"></a>

Update documentation project theme configured at the organization level

**API Endpoint**: `PUT /organization/theme`

#### Synchronous Client

```python
from os import getenv
from sideko_portal import SidekoClient

client = SidekoClient(api_key=getenv("API_KEY"), session_cookie=getenv("API_KEY"))
res = client.org.theme.update(
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
res = await client.org.theme.update(
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
