import asyncio
from .rdkit_helper import main as server_main

__version__ = "0.1.0"

def main():
    """Main entry point for the package."""
    asyncio.run(server_main())