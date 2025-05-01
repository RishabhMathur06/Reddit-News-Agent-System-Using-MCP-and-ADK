import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

async def create_agent():
    """Creates the TTS Speaker agent by connecting to the ElevenLabs MCP server via uvx."""
    
    print("--- Attempting to start and connect to elevenlabs-mcp via uvx ---")

    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command='uvx',
            args=['elevenlabs-mcp'],
            env={'ELEVENLABS_API_KEY': os.environ.get('ELEVENLABS_API_KEY', '')}
        )
    )

    print(f"--- Connected to elevenlabs-mcp. Discovered {len(tools)} tool(s). ---")
    for tool in tools:
        print(f"  - Discovered tool: {tool.name}")

    llm = LiteLlm(model="gemini/gemini-2.5-flash-preview-04-17", api_key=os.environ.get("GOOGLE_API_KEY"))

    # Defining the TTS Speaker Agent configurations
    agent_instance = Agent(
        name="tts_speaker_agent",
        description="Converts provided text into speech using ElevenLabs TTS MCP.",
        instruction=(
            "You are a Text-to-Speech agent. Take the text provided by the user or coordinator and "
            "use the available ElevenLabs TTS tool to convert it into audio. "
            "When calling the text_to_speech tool, set the parameter 'voice_name' to 'Will'. "
            "Return the result from the tool (expected to be a URL)."
        ),
        model=llm,
        tools=tools
    )

    return agent_instance, exit_stack

root_agent = create_agent()