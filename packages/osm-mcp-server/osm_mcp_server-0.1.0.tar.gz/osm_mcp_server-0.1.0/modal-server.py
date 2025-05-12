# modal-server.py
import modal
import os

from mcp_sdk.mcp_server import MCPServer
from mcp_sdk.transports.http import create_asgi_app as create_http_asgi_app
from mcp_sdk.transports.sse import create_asgi_app as create_sse_asgi_app

# Assuming your OSMMCP server class is defined in osm_mcp_server.server
# Adjust the import path if your project structure is different.
# For this example, let's assume a placeholder OSMMCP class if the actual one isn't available yet.
try:
    from osm_mcp_server.server import OSMMCP
except ImportError:
    print("Warning: OSMMCP class not found. Using a placeholder. Ensure osm_mcp_server.server.OSMMCP is correctly defined.")
    class OSMMCP(MCPServer):
        def __init__(self):
            super().__init__(tools=[]) # Initialize with no tools if placeholder
            print("Initialized Placeholder OSMMCP")

        async def _get_tool_instance(self, tool_name: str):
            # Placeholder: In a real scenario, this would return an instance of your tool
            print(f"Placeholder: Tool '{tool_name}' requested, but no tools are defined.")
            return None

# Define the Modal Image with dependencies from pyproject.toml
# Ensure osmnx cache directory is configured


stub = modal.Stub(name="osm-mcp-server-modal") # Changed from App to Stub for newer Modal versions

# Define a persistent volume for osmnx caching
cache_volume = modal.Volume.persisted("osmnx-cache-vol")

# Define the image for the Modal functions
# We list dependencies explicitly here. For a real project, you might sync with pyproject.toml
# or use a Dockerfile for more complex setups.
osm_mcp_server_image = modal.Image.debian_slim(python_version="3.11").pip_install(".").env({
    "OSMNX_CACHE_FOLDER": "/cache/osmnx_cache" # Ensure env var is set inside the container
})

# Initialize your OSMMCP server instance
# This instance will be shared by the handlers if defined at the stub level
# or created per request if initialized within the handler.
# For shared state and efficiency, initialize it once.
# Note: If OSMMCP has async setup, it might need to be handled within an async context or lifecycle hook.
mcp_server_instance = OSMMCP()

# Create ASGI apps for HTTP and SSE transports
http_asgi_app = create_http_asgi_app(mcp_server_instance)
sse_asgi_app = create_sse_asgi_app(mcp_server_instance)

# Streamable HTTP endpoint
@stub.asgi_app(
    image=osm_mcp_server_image,
    volumes={"/cache": cache_volume},
    keep_warm=1, # For cold start mitigation
    secrets=[modal.Secret.from_name("my-modal-secrets", optional=True)] # Example for secrets
)
async def mcp_streamable_http_handler():
    print(f"OSMNX_CACHE_FOLDER in HTTP handler: {os.getenv('OSMNX_CACHE_FOLDER')}")
    # Ensure cache directory exists
    cache_dir = os.getenv("OSMNX_CACHE_FOLDER", "/cache/osmnx_cache")
    os.makedirs(cache_dir, exist_ok=True)
    print(f"Cache directory '{cache_dir}' ensured.")
    return http_asgi_app

# SSE endpoint
@stub.asgi_app(
    image=osm_mcp_server_image,
    volumes={"/cache": cache_volume},
    keep_warm=1, # For cold start mitigation
    secrets=[modal.Secret.from_name("my-modal-secrets", optional=True)] # Example for secrets
)
async def mcp_sse_handler():
    print(f"OSMNX_CACHE_FOLDER in SSE handler: {os.getenv('OSMNX_CACHE_FOLDER')}")
    # Ensure cache directory exists
    cache_dir = os.getenv("OSMNX_CACHE_FOLDER", "/cache/osmnx_cache")
    os.makedirs(cache_dir, exist_ok=True)
    print(f"Cache directory '{cache_dir}' ensured.")
    return sse_asgi_app

# Optional: A simple health check endpoint
@stub.function(image=osm_mcp_server_image)
@modal.web_endpoint(method="GET")
async def health():
    return {"status": "ok", "message": "OSM MCP Server is running"}

# To deploy (from your terminal, not in this script):
# modal deploy modal-server.py

# To get the URL of your deployed app (after deployment):
# modal url osm-mcp-server-modal.mcp_streamable_http_handler
# modal url osm-mcp-server-modal.mcp_sse_handler