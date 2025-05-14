from mcp.server.fastmcp import FastMCP
import pandas as pd
import os
import asyncio
from importlib.resources import files

mcp = FastMCP("server_stdio MCP Demo")


@mcp.tool()
def exponential(a: int, b: int) -> int:
    """Return a^b."""
    return a**b


@mcp.tool()
def get_greeting(name: str) -> str:
    """Returns a greeting for the given name."""
    return f"Hello, {name}!"


@mcp.tool()
def get_psilo_data(project_name: str) -> list[dict]:
    """Returns psilo data filtered by project name."""
    try:
        print("--------INSIDE get_psilo_data---------")
        # Locate the CSV inside the package
        csv_path = files("mcp_psilo_mock").joinpath("fake_psilo_data.csv")

        print(f"[DEBUG] CSV path: {csv_path}")
        print(f"[DEBUG] File exists? {csv_path.exists()}")

        df = pd.read_csv(csv_path)

        print(f"[DEBUG] DataFrame loaded: {len(df)} rows")
        print(f"[DEBUG] Columns: {list(df.columns)}")

        filtered_df = df[df["Project"] == project_name]
        print(f"[DEBUG] Filtered rows for '{project_name}': {len(filtered_df)}")

        return [
            {
                "pdb_id": row["PDB_ids"],
                "date": row["Dates"],
                "project": row["Project"],
                "title": row["Title"],
            }
            for _, row in filtered_df.iterrows()
        ]
    except Exception as e:
        print(f"[ERROR] Failed to load or filter data: {str(e)}")
        return [{"error": f"Failed to load data: {str(e)}"}]


async def debug_list_tools():
    tools = await mcp.list_tools()
    for tool in tools:
        print(f" - {tool.name}")


def print_registered_tools():
    print("List of registered tools:")
    asyncio.run(debug_list_tools())
    print("Script complete")


def run_server():
    print_registered_tools()
    print("Starting MCP server...")
    mcp.run()


if __name__ == "__main__":
    run_server()
