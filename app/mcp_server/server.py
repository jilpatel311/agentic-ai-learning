from mcp.server.fastmcp import FastMCP

from app.mcp_server.config import SERVER_NAME

from app.mcp_server.tools.calculator import calculate

mcp = FastMCP(
    SERVER_NAME,
)


@mcp.tool()
def calculator(
    expression: str,
) -> str:
    """
    Calculate a mathematical expression.
    """

    return calculate(
        expression
    )


def main():

    mcp.run(
        transport="streamable-http"
    )


if __name__ == "__main__":
    main()