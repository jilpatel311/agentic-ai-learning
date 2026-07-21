import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


class MCPClientService:

    def __init__(
        self,
        server_url: str = "http://127.0.0.1:8000/mcp",
    ):
        self.server_url = server_url

    async def _call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):

        async with streamable_http_client(
            self.server_url
        ) as (
            read_stream,
            write_stream,
            _,
        ):

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    arguments,
                )

                return result

    def call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):

        return asyncio.run(
            self._call_tool(
                tool_name,
                arguments,
            )
        )