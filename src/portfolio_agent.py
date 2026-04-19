import os
import sys

from pydantic import SecretStr

from openhands.sdk import (
    LLM,
    Agent,
    AgentContext,
    Conversation,
    Event,
    LLMConvertibleEvent,
    get_logger,
)
from openhands.sdk.context import Skill, KeywordTrigger
from openhands.sdk.tool import Tool
from openhands.tools.terminal import TerminalTool

logger = get_logger(__name__)

def main():
    # Configure LLM
    api_key = os.getenv("LLM_API_KEY",None)
        
    model = os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929")
    base_url = os.getenv("LLM_BASE_URL")
    
    llm = LLM(
        usage_id="portfolio-agent",
        model=model,
        base_url=base_url,
        api_key=SecretStr(api_key),
    )

    # Load Skills from markdown files
    skills = []
    strategies_dir = os.path.join(os.getcwd(), "strategies")
    if os.path.exists(strategies_dir):
        for filename in os.listdir(strategies_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(strategies_dir, filename)
                with open(file_path, "r") as f:
                    content = f.read()
                
                # Derive keyword from filename (e.g., value_investing.md -> value investing)
                keyword = filename.replace(".md", "").replace("_", " ")
                
                skills.append(
                    Skill(
                        name=filename,
                        content=content,
                        source=file_path,
                        # Trigger when the strategy name is mentioned
                        trigger=KeywordTrigger(keywords=[keyword]),
                    )
                )

    # Configure Agent Context
    agent_context = AgentContext(
        skills=skills,
        system_message_suffix=(
            "You are a helpful Portfolio Manager Agent. "
            "You can execute various operations like fetching holdings, "
            "analyzing the portfolio, or placing orders using the configured Zerodha Kite MCP server. "
            "If a user asks about a specific strategy, check if you have a relevant skill loaded."
        )
    )

    # Setup Tools
    tools = [
        Tool(
            name=TerminalTool.name,
            params={"no_change_timeout_seconds": 5},
        )
    ]

    # Setup MCP Configuration for Zerodha
    mcp_config = {
        "mcpServers": {
            "ZerodhaKite": {
                "command": "npx",
                "args":["mcp-remote","https://mcp.kite.trade/mcp",], 
                "auth": "oauth", # Assuming OAuth based on the example
            }

        }
    }

    # Initialize Agent
    agent = Agent(llm=llm, tools=tools, mcp_config=mcp_config, agent_context=agent_context)

    # Define a callback to handle displaying the agent's responses
    def conversation_callback(event: Event):
        if isinstance(event, LLMConvertibleEvent):
            msg = event.to_llm_message()
            # Only print messages from the assistant
            if msg.role == "assistant":
                # Assuming msg.content is a list of blocks or a string
                if isinstance(msg.content, list):
                    for block in msg.content:
                        if block.type == "text":
                            print(f"\n[Agent]: {block.text}")
                elif isinstance(msg.content, str):
                    print(f"\n[Agent]: {msg.content}")

    # Initialize Conversation
    cwd = f"{os.getcwd()}/workspace"
    conversation = Conversation(
        agent=agent, 
        callbacks=[conversation_callback], 
        workspace=cwd
    )

    print("=" * 60)
    print("Welcome to the Portfolio Manager Agent CLI!")
    print("Supported operations: login, get profile, get holdings, analyse portfolio, etc.")
    print("Type 'exit' or 'quit' to close the application.")
    print(f"Loaded {len(skills)} trading strategies as skills.")
    print("=" * 60)

    # Interactive loop
    while True:
        try:
            user_input = input("\n[You]: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting Portfolio Manager Agent. Goodbye!")
                break
                
            # Send message and run
            conversation.send_message(user_input)
            conversation.run()
            
        except KeyboardInterrupt:
            print("\nExiting Portfolio Manager Agent. Goodbye!")
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
