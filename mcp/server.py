from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "AI Employee Assistant"
)


@mcp.tool()
def hello(name: str) -> str:
    """
    Simple demo tool.
    """

    return f"Hello {name}!"


if __name__ == "__main__":
    mcp.run()