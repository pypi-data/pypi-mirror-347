import json
from mcp.server.fastmcp import FastMCP
import pandas as pd
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


# # -----------------------------------------------
# # 🔧 TEMPORARY WORKAROUND FOR MISSING SCHEMAS
# # This dictionary hardcodes the parameter schemas
# # until MCP STDIO includes them via parametersSchema.
# # Replace this with `tool.parametersSchema` once supported.
# # -----------------------------------------------
# @mcp.tool()
# def list_tool_parameters() -> dict:
#     return {
#         "exponential": {"a": {"type": "integer"}, "b": {"type": "integer"}},
#         "get_greeting": {"name": {"type": "string"}},
#         "get_psilo_data": {"project_name": {"type": "string"}},
#     }


# --- Server startup utilities ---


async def debug_list_tools():
    tools = await mcp.list_tools()

    print(f"Returned tools: {tools}")
    for tool in tools:
        print(f" - {tool.name}")
        print(f"    Description: {tool.description}")

        # Pull inputSchema directly
        input_schema = getattr(tool, "inputSchema", {})
        print(f"    inputSchema: {json.dumps(input_schema, indent=4)}")


def print_registered_tools():
    print("-------------------------------------------------")
    print("List of registered tools:")
    asyncio.run(debug_list_tools())
    print("-------------------------------------------------")

    # print("Manual schema (temporary fix)")
    # # Call your custom tool directly (as a function)
    # schema = list_tool_parameters()
    # for tool_name, params in schema.items():
    #     print(f"{tool_name}")
    #     for param, meta in params.items():
    #         arg_type = meta.get("type", "string")
    #         print(f"  - {param} ({arg_type})")
    #     if not params:
    #         print("  (No parameters)")
    #     print()
    # print()
    # print("Script complete")


def run_server():
    print_registered_tools()
    print("Starting MCP server...")
    mcp.run()


if __name__ == "__main__":
    run_server()
