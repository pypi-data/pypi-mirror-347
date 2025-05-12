# osm_mcp_server/__init__.py
import asyncio
import logging

# Ensure relative imports work correctly. 
# The console script defined in pyproject.toml (`osm-mcp-server = "osm_mcp_server:main"`)
# will execute this main() function.

try:
    from .server import OSMMCP
except ImportError as e:
    # This path might be taken if the package is not installed correctly (e.g., `pip install -e .` not run)
    # or if there's an issue within .server module itself.
    logging.basicConfig(level=logging.ERROR)
    logging.error(f"Failed to import OSMMCP from .server: {e}. Ensure the package is installed correctly (e.g., pip install -e .).", exc_info=True)
    # Optionally, re-raise or exit if the server cannot start without OSMMCP
    raise # Or import sys; sys.exit(1)

# mcp_sdk.stdio_server is part of the base mcp-sdk.
from mcp_sdk.stdio_server import run_stdio_server

def main():
    """
    Entry point for the osm-mcp-server console script.
    Initializes and runs the OSMMCP server over stdio.
    """
    # Configure logging for the console script.
    # Customize the logging level and format as needed.
    logging.basicConfig(
        level=logging.INFO, # Change to logging.DEBUG for more verbose output during development
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("osm-mcp-server.script") # Specific logger for the script's operations
    
    logger.info("Initializing OSMMCP server for stdio communication...")

    try:
        # Create an instance of your MCP server
        server_instance = OSMMCP()
        logger.info("OSMMCP server instance created successfully.")
        
        logger.info("Starting stdio server loop...")
        # Run the server using asyncio and the stdio transport from mcp-sdk
        asyncio.run(run_stdio_server(server_instance))
        
    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C
        logger.info("Server process interrupted by user (Ctrl+C). Shutting down gracefully.")
    except ImportError as e:
        # This might catch the re-raised ImportError from above if not handled there
        logger.error(f"Import error during server initialization: {e}. Please check dependencies and installation.", exc_info=True)
    except Exception as e:
        # Catch any other unexpected errors during server execution
        logger.error(f"An unexpected error occurred while running the server: {e}", exc_info=True)
    finally:
        # This block will execute after the server loop finishes or an exception is handled
        logger.info("OSMMCP server has shut down.")

# The following block allows running `python -m osm_mcp_server` (if osm_mcp_server is a directory in PYTHONPATH)
# However, the primary entry point for users will be the console script `osm-mcp-server` 
# after installing the package.
if __name__ == '__main__':
    # This part is generally not hit when running as an installed console script,
    # but can be useful for certain development/testing scenarios.
    # Re-initialize basicConfig here if not already configured by a higher-level entry point
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    logger = logging.getLogger(__name__) # Logger for this specific execution context
    logger.info(f"Running {__name__} directly (e.g., via python -m osm_mcp_server). Calling main().")
    main()