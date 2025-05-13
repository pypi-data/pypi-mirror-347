import asyncio
from contextlib import AbstractAsyncContextManager, AsyncExitStack
from typing import Any, Literal

from coagent.core import BaseAgent, Context, handler, logger, Message
from coagent.core.messages import Cancel
from coagent.core.exceptions import InternalError
from mcp import ClientSession, Tool as MCPTool  # noqa: F401
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.types import (
    CallToolResult as MCPCallToolResult,
    ListToolsResult as MCPListToolsResult,
    ImageContent as MCPImageContent,  # noqa: F401
    TextContent as MCPTextContent,  # noqa: F401
)
from pydantic import BaseModel


# An alias of `mcp.client.stdio.StdioServerParameters`.
MCPServerStdioParams = StdioServerParameters


class MCPServerSSEParams(BaseModel):
    """Core parameters in `mcp.client.sse.sse_client`."""

    url: str
    """The URL of the server."""

    headers: dict[str, str] | None = None
    """The headers to send to the server."""


class Connect(Message):
    """A message to connect to the server.

    To close the server, send a `Close` message to close the connection
    and delete corresponding server agent.
    """

    transport: Literal["sse", "stdio"]
    """The transport to use.

    See https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/transports/.
    """

    params: MCPServerStdioParams | MCPServerSSEParams
    """The parameters to connect to the server."""

    enable_cache: bool = True
    """Whether to cache the list result. Defaults to `True`.
    
    If `True`, the tools list will be cached and only fetched from the server
    once. If `False`, the tools list will be fetched from the server on each
    `ListTools` message. The cache can be invalidated by sending an
    `InvalidateCache` message.
    
    Only set this to `False` if you know the server will change its tools list,
    because it can drastically increase latency (by introducing a round-trip
    to the server every time).
    """


# A message to close the server.
#
# Note that this is an alias of the `Cancel` message since it's ok to close
# the server by deleting the corresponding agent.
Close = Cancel


class InvalidateCache(Message):
    """A message to invalidate the cache of the list result."""

    pass


class ListTools(Message):
    """A message to list the tools available on the server."""

    pass


class ListToolsResult(Message, MCPListToolsResult):
    """The result of `ListTools`."""

    pass


class CallTool(Message):
    """A message to call a tool on the server."""

    name: str
    """The name of the tool to call."""

    arguments: dict[str, Any] | None = None
    """The arguments to pass to the tool."""


class CallToolResult(Message, MCPCallToolResult):
    """The result of `ListTools`."""

    pass


class MCPServer(BaseAgent):
    """An agent that acts as an MCP client to connect to an MCP server."""

    def __init__(self, timeout: int = float("inf")) -> None:
        super().__init__(timeout=timeout)

        self._client_session: ClientSession | None = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()

        self._list_tools_result_cache: ListToolsResult | None = None
        self._cache_enabled: bool = False
        self._cache_invalidated: bool = False

        # Ongoing tasks that need to be cancelled when the server is stopped.
        self._pending_tasks: set[asyncio.Task] = set()

    async def stopped(self) -> None:
        await self._cleanup()

    async def _handle_data(self) -> None:
        """Override the method to handle exceptions properly."""
        try:
            await super()._handle_data()
        finally:
            # Ensure the resources are properly cleaned up.
            await self._cleanup()

    async def _handle_data_custom(self, msg: Message, ctx: Context) -> None:
        """Override to handle `ListTools` and `CallTool` messages concurrently."""
        match msg:
            case ListTools() | CallTool():
                task = asyncio.create_task(super()._handle_data_custom(msg, ctx))
                self._pending_tasks.add(task)
                task.add_done_callback(self._pending_tasks.discard)
            case _:
                await super()._handle_data_custom(msg, ctx)

    @handler
    async def connect(self, msg: Connect, ctx: Context) -> None:
        """Connect to the server."""
        if msg.transport == "sse":
            ctx_manager: AbstractAsyncContextManager = sse_client(
                **msg.params.model_dump()
            )
        else:  # "stdio":
            ctx_manager: AbstractAsyncContextManager = stdio_client(msg.params)

        try:
            transport = await self._exit_stack.enter_async_context(ctx_manager)
            read, write = transport
            session = await self._exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await session.initialize()

            self._client_session = session
            self._cache_enabled = msg.enable_cache
        except Exception as exc:
            logger.error(f"Error initializing MCP server: {exc}")
            await self._cleanup()
            raise

    @handler
    async def invalidate_cache(self, msg: InvalidateCache, ctx: Context) -> None:
        self._cache_invalidated = True

    @handler
    async def list_tools(self, msg: ListTools, ctx: Context) -> ListToolsResult:
        if not self._client_session:
            raise InternalError(
                "Server not initialized. Make sure to send the `Connect` message first."
            )

        # Return the cached result if the cache is enabled and not invalidated.
        if (
            self._cache_enabled
            and not self._cache_invalidated
            and self._list_tools_result_cache
        ):
            return self._list_tools_result_cache

        # Reset the cache status.
        self._cache_invalidated = False

        result = await self._client_session.list_tools()
        self._list_tools_result_cache = ListToolsResult(**result.model_dump())
        return self._list_tools_result_cache

    @handler
    async def call_tool(self, msg: CallTool, ctx: Context) -> CallToolResult:
        if not self._client_session:
            raise InternalError(
                "Server not initialized. Make sure to send the `Connect` message first."
            )

        result = await self._client_session.call_tool(msg.name, arguments=msg.arguments)
        return CallToolResult(**result.model_dump())

    async def _cleanup(self) -> None:
        """Cleanup the server."""
        if self._pending_tasks:
            # Cancel all pending tasks.
            for task in self._pending_tasks:
                task.cancel()

        if not self._client_session:
            return

        try:
            await self._exit_stack.aclose()
            self._client_session = None
        except Exception as exc:
            logger.error(f"Error cleaning up server: {exc}")
