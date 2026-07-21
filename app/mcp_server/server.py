from mcp.server.fastmcp import FastMCP

from app.mcp_server.config import SERVER_NAME
from app.mcp_server.tools.calculator import CalculatorTool


mcp = FastMCP(SERVER_NAME)

calculator_tool = CalculatorTool()


@mcp.tool()
def calculator(
    expression: str,
) -> str:
    """
    Calculate a mathematical expression.
    """

    result = calculator_tool.calculate(
        expression
    )

    return str(result)


def main():

    mcp.run(
        transport="streamable-http"
    )


if __name__ == "__main__":
    main()