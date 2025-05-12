"""
Main entry point for the Telegram MCP package.

This module provides the main entry point for running the Telegram MCP package.
"""

import sys
import asyncio
import sqlite3
import nest_asyncio
from .client import client, mcp

def main():
    """Main entry point for the Telegram MCP package."""
    nest_asyncio.apply()
    
    async def async_main() -> None:
        try:
            # Start the Telethon client non-interactively
            print("Starting Telegram client...")
            await client.start()

            print("Telegram client started. Running MCP server...")
            # Use the asynchronous entrypoint
            await mcp.run_stdio_async()
        except Exception as e:
            print(f"Error starting client: {e}", file=sys.stderr)
            if isinstance(e, sqlite3.OperationalError) and "database is locked" in str(e):
                print(
                    "Database lock detected. Please ensure no other instances are running.",
                    file=sys.stderr,
                )
            sys.exit(1)

    asyncio.run(async_main())


if __name__ == "__main__":
    main()
