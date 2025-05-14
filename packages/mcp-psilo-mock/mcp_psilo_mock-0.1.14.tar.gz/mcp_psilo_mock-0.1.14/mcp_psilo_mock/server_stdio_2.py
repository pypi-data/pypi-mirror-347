from mcp.server.fastmcp import FastMCP
import asyncio

mcp = FastMCP("server_stdio2")


@mcp.tool()
def exponent(a: int, b: int) -> int:
    """Return a raised to the power of b."""
    print(f"[SERVER] exponent({a}, {b}) called")
    return a**b


async def debug_list_tools():
    tools = await mcp.list_tools()
    for tool in tools:
        print(f"[SERVER] Tool registered: {tool.name}")


def safe_run_async(coro):
    try:
        asyncio.run(coro)
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            import nest_asyncio

            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(coro)
        else:
            raise


def print_registered_tools():
    print("[SERVER] Listing registered tools:")
    safe_run_async(debug_list_tools())
    print("[SERVER] Done listing tools.")


def run_server():
    print_registered_tools()
    print("[SERVER] Starting MCP stdio server...")
    mcp.run()


if __name__ == "__main__":
    run_server()
