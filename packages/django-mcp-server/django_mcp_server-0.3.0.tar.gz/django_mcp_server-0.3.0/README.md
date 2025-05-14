# Django MCP Server

[![PyPI version](https://img.shields.io/pypi/v/django-mcp-server)](https://pypi.org/project/django-mcp-server/)
![License](https://img.shields.io/pypi/l/django-mcp-server)
[![Published on Django Packages](https://img.shields.io/badge/Published%20on-Django%20Packages-0c3c26)](https://djangopackages.org/packages/p/django-mcp-server/)
![Python versions](https://img.shields.io/pypi/pyversions/django-mcp-server)
[![Django versions](https://img.shields.io/pypi/frameworkversions/django/django-mcp-server)](https://pypi.org/project/django-mcp-server/)

**Django MCP Server** is an implementation of the **Model Context Protocol (MCP)** extension for Django. This module allows **MCP Clients** and **AI agents** to interact with **any Django application** seamlessly.

✅ Works inside your existing **WSGI** application.  
🚀 Implements the standare stdio and **Streamable HTTP transport (stateless)** is implemented. 
🤖 Any MCP Client, including Claude Desktop can interact with your application.

Licensed under the **MIT License**.

---

## Features

- Expose Django models and logic as **MCP tools**.
- Serve an MCP endpoint inside your Django app.
- Easily integrate with AI agents, MCP Clients, or tools like Google ADK.

---

## Quick Start

### 1️⃣ Install

```bash
pip install django-mcp-server
```

Or directly from GitHub:

```bash
pip install git+https://github.com/omarbenhamid/django-mcp-server.git
```

---

### 2️⃣ Configure Django

✅ Add `mcp_server` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # your apps...
    'mcp_server',
]
```

✅ Add the **MCP endpoint** to your `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # your urls...
    path("", include('mcp_server.urls')),
]
```

By default, the MCP endpoint will be available at `/mcp`.

---

### 3️⃣ Define MCP Tools

Create a file `mcp.py` in your Django app and create a sub class of MCPToolset : each method that does
not start with "_" will be published as a tool.

Example:
```python
from mcp_server import MCPToolset

class MyAITools(MCPToolset):
    # This method will not be published as a tool because it starts with _
    def add(self, a: int, b: int) -> list[dict]:
        """A service to add two numbers together"""
        return a+b

    def generate_welcome_message(self, name) -> str:
        return "Hi {name}, welcom by Django MCP Server"

    def send_email(self, to_email: str, subject: str, body: str):
        """ A tool to send emails"""
        from django.core.mail import send_mail

        send_mail(
             subject=subject,
             message=body,
             from_email='your_email@example.com',
             recipient_list=[to_email],
             fail_silently=False,
         )
```

---

### Use the MCP Tool

The mcp tool is now published on your Django App at `/mcp` endpoint. You can 
test it with the python mcp SDK :

```python
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession


async def main():
    # Connect to a streamable HTTP server
    async with streamablehttp_client("http://localhost:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            # Call a tool
            tool_result = await session.call_tool("get_alerts", {"state": "NY"})
            print(tool_result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

Replace `http://localhost:8000/mcp` by the acutal Django host and run this cript.

### Test in Claude Desktop

You can [test MCP servers in Claude Desktop](https://modelcontextprotocol.io/quickstart/server). As for now
claude desktop only supports local MCP Servers. So you need to have your app installed on the same machine, in a
dev setting probably.

For this you need :

1. To install Claude Desktop from [claude.ai](https://claude.ai)
2. Open File > Settings > Developer and click **Edit Config**
3. Open `claude_desktop_config.json` and setup your MCP server :
   ```json
   {
    "mcpServers": {
        "test_django_mcp": {
            "command": "/path/to/interpreter/python",
            "args": [
                "/path/to/your/project/manage.py",
                "stdio_server"
            ]
        }
    }
   ```

**NOTE** `/path/to/interpreter/` should point to a python interpreter you use (can be in your venv for example)
and `/path/to/your/project/` is the path to your django project.



## Advanced topics

### Django Rest Framework Serializer integration

You can annotate a tool with `drf_serialize_output(...)` to serialize its output using
django rest framework, like : 

```python
from mcp_server import drf_serialize_output
from .serializers import FooBarSerializer
from .models import FooBar

class MyTools(MCPToolset):
   @drf_serialize_output(FooBarSerializer)
   def get_foo_bar():
       return FooBar.objects.first()
```

### Use low level mcp server annotation

You can import the DjangoMCP server instance and use FastMCP annotations to declare
mcp tools and resources :

```python
from mcp_server import mcp_server as mcp
from .models import Bird


@mcp.tool()
async def get_species_count(name: str) -> int:
    '''Find the ID of a bird species by name (partial match). Returns the count.'''
    ret = await Bird.objects.filter(species__icontains=name).afirst()
    if ret is None:
        ret = await Bird.objects.acreate(species=name)
    return ret.count

@mcp.tool()
async def increment_species(name: str, amount: int = 1) -> int:
    '''
    Increment the count of a bird species by a specified amount.
    Returns the new count.
    '''
    ret = await Bird.objects.filter(species__icontains=name).afirst()
    if ret is None:
        ret = await Bird.objects.acreate(species=name)
    ret.count += amount
    await ret.asave()
    return ret.count
```

⚠️ **Important**:
1. Always use **Django's async ORM API** when you define async tools.
2. Be careful not to return a QuerySet as it will be evaluated asynchroniously which would create errors.

### Customize the default MCP server settings

In `settings.py` you can initialize the `DJANGO_MCP_GLOBAL_SERVER_CONFIG` parameter. These will be 
passed to the `MCPServer` server during initialization
```python
DJANGO_MCP_GLOBAL_SERVER_CONFIG = {
    "name":"mymcp",
    "instructions": "Some instructions to use this server",
    "stateless": False
}
```


### Session management

By default the server is statefull, and state is managed as [Django session](https://docs.djangoproject.com/en/5.2/topics/http/sessions/)
`request.session` object, so the session backend must thus be set up correctly. The 
request object is available in `self.request` for class based toolsets.

**NOTE** The session middleware is not required to be set up as MCP sessions are managed
independently and without cookies.
. 
You can make the server stateless by defining : `DJANGO_MCP_GLOBAL_SERVER_CONFIG`

**IMPORTANT** state is managed by django sessions, if you use low level `@mcp_server.tool()` annotation for example
the behaviour of preserving the server instance accross calls of the base python API is not preserved due to architecture
of django in WSGI deployments where requests can be served by different threads !

### Authorization

The MCP endpoint supports [Django Rest Framework authorization classes](https://www.django-rest-framework.org/api-guide/authentication/)
You can set them using `DJANGO_MCP_AUTHENTICATION_CLASSES` in `settings.py` ex. :

```python
DJANGO_MCP_AUTHENTICATION_CLASSES=["rest_framework.authentication.TokenAuthentication"]
```

**IMPORTANT** Now the [MCP Specification version 2025-03-26](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization)
advices to use an OAuth2 workflow, so you should integrate 
[django-oauth-toolkit with djangorestframework integration](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html) 
setup, and use `'oauth2_provider.contrib.rest_framework.OAuth2Authentication'` in
`DJANGO_MCP_AUTHENTICATION_CLASSES`. Refer to [the official documentation of django-oauth-toolkit](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html) 

### Advanced / customized setup of the view

You can in your urls.py mount the MCPServerStreamableHttpView.as_view() view and customize it with any extra parameters.

### Secondary MCP endpoint
in `mcp.py`
```python

second_mcp = DjangoMCP(name="altserver")

@second_mcp.tools()
async def my_tool():
    ...
```

in urls.py 
```python
...
    path("altmcp", MCPServerStreamableHttpView.as_view(mcp_server=second_server))
...
```

**IMPORTANT** When you do this the DJANGO_MCP_AUTHENTICATION_CLASSES settings is **ignored** and 
your view is unsecure. You **SHOULD** [Setup DRF Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
for your view, for exemple : 
```python
...
MCPServerStreamableHttpView.as_view(permission_classes=[IsAuthenticated], authentication_classes=[TokenAuthentication])
...
```

## Testing

### The server
You can setup you own app or use the [mcpexample django app](examples/mcpexample) app.

### The client

By default, your MCP Server will be available as a 
[stateless streamable http transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http) 
endpoint at <your_django_server>/mcp (ex. http://localhost:8000/mcp) (*without / at the end !).

There are many ways to test :

1. Using the test [MCP Client script : test/test_mcp_client.py](test/test_mcp_client.py)  
2. You can test using [MCP Inspector tool](https://github.com/modelcontextprotocol/inspector) 
3. or any compatible MCP Client like google agent developement kit.

---

## Integration with Agentic Frameworks and MCP Clients

### Google Agent Developement Kit Example

**NOTE** as of today the [official google adk does not support StreamableHTTP Transport](https://github.com/google/adk-python/issues/479) 
but you could use [this fork](https://github.com/omarbenhamid/google-adk-python)

Then you can use the [test agent in test/test_agent](test/test_agent/agent.py) with by 
starting `adk web` in the `test` folder. Make sure first : 

1. Install adk with streamablehttp support : `pip install git+https://github.com/omarbenhamid/google-adk-python.git`
2. Start a django app with an MCP endpoint : `python manage.py runserver` in the `examples/mcpexample` folder.
2. If you use TokenAuthorization create an access token, for example in Django Admin of your app.
3. Setup in `test/test_agent/agent.py` the right endpoint location and authentication header
4. Enter the `test` folder.
5. Run `adk web`
6. In the shell you can for example use this prompt : "I saw woody woodpecker, add it to my inventory"


### Other clients
You can easily plug your MCP server endpoint into any agentic framework supporting MCP streamable http servers.
Refer to this [list of clients](https://modelcontextprotocol.io/clients)

---

## Roadmap

- ✅ **Stateless streamable HTTP transport** (implemented)
- 🔜 **STDIO transport integration for dev configuration (ex. Claude Desktop)**
- 🔜 ****
- 🔜 **Stateful streamable HTTP transport using Django sessions**
- 🔜 **SSE endpoint integration (requires ASGI)**
- 🔜 **Improved error management and logging**

---

## Issues

If you encounter bugs or have feature requests, please open an issue on [GitHub Issues](https://github.com/omarbenhamid/django-mcp-server/issues).

---

## License

MIT License.
