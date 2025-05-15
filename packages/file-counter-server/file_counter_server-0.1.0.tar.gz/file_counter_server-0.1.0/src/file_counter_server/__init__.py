from .mcp import mcp


def main() -> None:
    print("Hello from file-counter-server!")
    mcp.run(transport="stdio")
