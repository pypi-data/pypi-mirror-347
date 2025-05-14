"""
Port MCP Gateway - A gateway for interacting with Port.io through a standardized MCP API
"""

__version__ = "0.0.1"

def get_version():
    """Return the package version."""
    return __version__

def main():
    """Main entry point."""
    print(f"Port MCP Gateway version {get_version()}")
    print("A gateway for interacting with Port.io through a standardized MCP API")

if __name__ == "__main__":
    main()
