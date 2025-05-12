# osm_mcp_server/server.py
import asyncio
import os
import logging
from typing import Any, Dict, Type

import osmnx as ox
from pydantic import BaseModel, Field

from mcp_sdk.mcp_server import MCPServer, Tool, ToolContext
from mcp_sdk.protocol_beta import Status, TaskStage, TaskStep, TextContent

# Configure osmnx logging and cache
# The cache folder is set by an environment variable in modal-server.py
ox.settings.log_console = True
# ox.settings.cache_folder: this will be picked from env var OSMNX_CACHE_FOLDER

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- Tool Input Schemas ---
class GetPlaceGraphInput(BaseModel):
    query: str = Field(..., description="The place query string (e.g., 'Manhattan, New York City, USA')")

# --- Tool Definitions ---
class GetPlaceGraph(Tool[GetPlaceGraphInput, None]):
    name: str = "get_place_graph_info"
    description: str = "Retrieves a street network graph for a specified place using OSMnx and returns basic information about it."
    input_schema: Type[GetPlaceGraphInput] = GetPlaceGraphInput
    # Output is streamed, so output_schema is None or a Pydantic model for the final summary if any.

    async def execute(self, input_data: GetPlaceGraphInput, context: ToolContext) -> None:
        query = input_data.query
        await context.send_status_update(
            TaskStep(
                stage=TaskStage.EXECUTING,
                status=Status.IN_PROGRESS,
                content=[TextContent(text=f"Fetching graph for query: {query}...")],
            )
        )

        try:
            logger.info(f"OSMnx cache folder: {ox.settings.cache_folder}")
            logger.info(f"Attempting to fetch graph for: {query}")

            # Running osmnx.graph_from_place in a separate thread to avoid blocking asyncio event loop
            # as osmnx can have synchronous I/O operations.
            loop = asyncio.get_event_loop()
            G = await loop.run_in_executor(None, ox.graph_from_place, query, network_type="drive")

            num_nodes = len(G.nodes)
            num_edges = len(G.edges)
            graph_info = f"Graph for '{query}' retrieved successfully.\nNodes: {num_nodes}\nEdges: {num_edges}"
            logger.info(graph_info)

            await context.send_status_update(
                TaskStep(
                    stage=TaskStage.EXECUTING,
                    status=Status.COMPLETED, # Or IN_PROGRESS if more steps follow
                    content=[TextContent(text=graph_info)],
                )
            )

        except Exception as e:
            error_message = f"Error fetching graph for '{query}': {str(e)}"
            logger.error(error_message, exc_info=True)
            await context.send_status_update(
                TaskStep(
                    stage=TaskStage.EXECUTING,
                    status=Status.ERRORED,
                    content=[TextContent(text=error_message)],
                )
            )
            raise

# --- OSMMCP Server Definition ---
class OSMMCP(MCPServer):
    def __init__(self):
        super().__init__(tools=[GetPlaceGraph()])
        logger.info("OSMMCP Server initialized with GetPlaceGraph tool.")
        cache_dir = os.getenv("OSMNX_CACHE_FOLDER")
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
            logger.info(f"Ensured OSMnx cache directory exists: {cache_dir}")
        else:
            logger.warning("OSMNX_CACHE_FOLDER environment variable not set. OSMnx will use default cache location.")

    async def _get_tool_instance(self, tool_name: str) -> Tool | None:
        for tool in self.tools:
            if tool.name == tool_name:
                logger.info(f"Returning instance of tool: {tool_name}")
                return tool
        logger.warning(f"Tool '{tool_name}' not found.")
        return None

# Example of how to run this server locally (not for Modal deployment, but for testing)
async def main_local():
    from mcp_sdk.stdio_server import run_stdio_server
    logging.basicConfig(level=logging.DEBUG)
    server = OSMMCP()
    await run_stdio_server(server)

if __name__ == "__main__":
    # This main is for local testing of the OSMMCP server logic itself,
    # not for how Modal runs it.
    # To run: python -m osm_mcp_server.server
    asyncio.run(main_local())