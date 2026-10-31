"""Run the MCP server with ``python -m revit_model_mcp``.

The console script ``revit-model-mcp`` and this module form start the same server, so tooling
that cannot rely on an installed entry point still reaches the registry.
"""

from .server import main

if __name__ == "__main__":
    main()
