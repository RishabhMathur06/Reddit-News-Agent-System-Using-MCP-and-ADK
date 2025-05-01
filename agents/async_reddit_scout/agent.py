# Importing dependencies
import asyncio
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from dotenv import load_dotenv

# Loading the environment variables.
load_dotenv()

# Function to get reddit tools from Reddit-MCP server.
async def get_tools_async():
    """Connects to the mcp-reddit server via uvx and returns the tools and exit stack."""

    print("--- Attempting to start and connect to mcp-reddit MCP server via uvx ---")

    try:
        # Check if uvx is available.
        # A more robust check might involve checking the actual command's success.
        await asyncio.create_subprocess_shell('uvx --version', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command='uvx',
                args=['--from', 'git+https://github.com/adhikasp/mcp-reddit.git', 'mcp-reddit'],

                # Optional: Add environment variables if needed by the MCP server, e.g., credentials if mcp-reddit required them.
                # env=os.environ.copy()
            )
        )

        print(f"--- Successfully connected to mcp-reddit server. Discovered {len(tools)} tool(s). ---")

        # Print discovered tool names for debugging/instruction refinement
        for tool in tools:
            print(f"  - Discovered tool: {tool.name}") # Tool name is likely 'fetch_reddit_hot_threads' or similar

        return tools, exit_stack

    except FileNotFoundError:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERROR: 'uvx' command not found. Please install uvx: pip install uvx !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # Return empty tools and a no-op exit stack to prevent agent failure
        class DummyExitStack:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass

        return [], DummyExitStack()

    except Exception as e:
        print(f"--- ERROR connecting to or starting mcp-reddit server: {e} ---")

        # Return empty tools and a no-op exit stack
        class DummyExitStack:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass

        return [], DummyExitStack()

#Function that initializes the root agent.
async def create_agent():
    '''Creating agent instance after fetching the tool from MCP server.'''

    tools, exit_stack = await get_tools_async()
    discovered_tool_name = "fetch_reddit_hot_threads"

    if not tools:
        print("--- WARNING: No tools discovered from the MCP server. Agent will lack Reddit functionality. ---")

    agent_instance = Agent(
        name="async_reddit_scout_agent",
        description = "A Reddit scout agent that searches for hot posts in a given subreddit using an external MCP Reddit tool.",
        model = "gemini-2.5-flash-preview-04-17",
        instruction=(
            "You are the Async Reddit News Scout. Your task is to fetch hot post titles from any subreddit using the connected Reddit MCP tool."
            "1. **Identify Subreddit:** Determine which subreddit the user wants news from. Default to 'gamedev' if none is specified. Use the specific subreddit mentioned (e.g., 'unity3d', 'unrealengine')."
            f"2. **Call Discovered Tool:** You **MUST** look for and call the tool named '{discovered_tool_name}' with the identified subreddit name and optionally a limit."
            "3. **Present Results:** The tool will return a formatted string containing the hot post information or an error message."
            "   - Present this string directly to the user."
            "   - Clearly state which subreddit the information is from."
            "   - If the tool returns an error message, relay that message accurately."
            "4. **Handle Missing Tool:** If you cannot find the required Reddit tool, inform the user that you cannot fetch Reddit news due to a configuration issue."
            "5. **Do Not Hallucinate:** Only provide information returned by the tool."
        ),
        tools=tools
    )

    return agent_instance, exit_stack

root_agent = create_agent()