import os
import sys
import uuid
from pydantic import SecretStr

from openhands.sdk import (
    LLM,
    Agent,
    AgentContext,
    Conversation,
    LLMSummarizingCondenser,
    Event,
    LLMConvertibleEvent,
    get_logger,
)

from openhands.sdk.context import Skill, KeywordTrigger
from openhands.sdk.tool import Tool, register_tool
from openhands.sdk.subagent import register_agent
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.delegate import DelegateTool, DelegationVisualizer
from openhands.tools import register_builtins_agents

logger = get_logger(__name__)

# Use a fixed namespace/name to generate a deterministic UUID for this specific agent.
# WARNING: If you switch Git branches and the available tools change (e.g., adding/removing tools),
# OpenHands will fail to resume the conversation from `./history` and raise a ValueError:
# 'Cannot resume conversation: tools were removed mid-conversation'.
# To fix this, simply delete the cached conversation in the `./history` directory.
CONSISTENT_ID = uuid.uuid5(uuid.NAMESPACE_DNS, "portfolio-manager-agent-unique-id")

def create_stock_picker_agent(llm: LLM) -> Agent:
    return Agent(
        llm=llm,
        tools=[Tool(name="TerminalTool"), Tool(name="FileEditorTool")],
        mcp_config=MCP_CONFIG,
        agent_context=AgentContext(
            system_message_suffix=(
                "You are a Stock Picker. Your goal is to find high momentum stocks from the current market. "
                "Follow the market trend to decide on the approach and alignment with leading sectors "
                "For each pick, fix the expected profit target and stop loss. "
                "Prefer pullback continuation opportunities after valid break of structure events. "
                "Prioritize stocks forming higher highs and higher lows with clean retracement behavior into demand zones. "
                "Quality and expectancy are more important than trade frequency."
                "Do not repeat information already provided."
                "Always check for existing positions before opening new ones. Avoid over-concentration. "
            )
        ),
    )

def create_technical_analysis_agent(llm: LLM) -> Agent:
    return Agent(
        llm=llm,
        tools=[Tool(name="TerminalTool")],
        agent_context=AgentContext(
            system_message_suffix=(
                "You are a professional technical analysis specialist focused on structure-based swing trading in the Indian equity market. "
                "Your responsibility is to analyze price structure, break of structure events, retracement quality, "
                "demand zones, support and resistance behavior, candle confirmation, trend strength, volatility conditions, "
                "and risk-reward characteristics. "
                "Always stick to the daily timeframe and use only clean, confirmed technical data. "
                "Your recommendations must follow the strict guidelines: Price > ₹100, Avg Volume > 1,000,000, and pre-earnings exclusion. "
                "Only consider stocks trading above both 20 EMA and 50 EMA with ADX > 25 and above average volume. "
                "Avoid stocks trading between EMAs or with low ADX. "
                "Every analysis must prioritize structure (BOS, PO3, retracements to demand/supply) and risk-adjusted probabilities. "
                "Use deterministic and objective price-action analysis instead of prediction-based assumptions. "
                "Do not repeat information already provided."
            )
        ),
    )

def create_order_execution_agent(llm: LLM) -> Agent:
    return Agent(
        llm=llm,
        tools=[Tool(name="TerminalTool")],
        mcp_config=MCP_CONFIG,
        agent_context=AgentContext(
            system_message_suffix=(
                "You are an Order Execution specialist. Execute and place orders (GTT or any other type) as requested. "
                "Your role is to ensure only fully validated, rule-compliant, high-quality trades are executed. "
                "Every trade must satisfy market regime, structure confirmation, liquidity, volatility, "
                "risk-reward, and portfolio exposure requirements before execution approval. "
                "Use Decimal (DECIMAL) type for price and quantity values to avoid float rounding errors."
                "Trade management must follow structure-based logic rather than arbitrary fixed-percentage exits. "
                "Order placement must use precise, non-rounded price and quantity values to avoid slippage. "
                "Execution discipline and capital protection take priority over trade frequency."
                "Do not repeat information already provided."
                "Avoid over-concentration." 
            )
        ),
    )

# Register sub-agents
register_agent(
    name="stock_picker",
    factory_func=create_stock_picker_agent,
    description="Identifies and recommends stocks for trading.",
)
register_agent(
    name="technical_analysis",
    factory_func=create_technical_analysis_agent,
    description="Provides analysis of stocks.",
)
register_agent(
    name="order_execution",
    factory_func=create_order_execution_agent,
    description="Executes and manages trades.",
)
register_builtins_agents()
register_tool("DelegateTool", DelegateTool)

def main():
    # Configure LLM
    api_key = os.getenv("LLM_API_KEY", None)
        
    model = os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929")
    base_url = os.getenv("LLM_BASE_URL")
    
    llm = LLM(
        usage_id="portfolio-agent",
        model=model,
        base_url=base_url,
        api_key=SecretStr(api_key),
    )

    condenser = LLMSummarizingCondenser(llm=llm, max_size=80, keep_first=8)

    # Load Skills from markdown files
    skills = []
    strategies_dir = os.path.join(os.path.dirname(__file__), "strategies")
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
            "You are the Orchestrator for the Portfolio Manager Agent system. "
            "You coordinate between specialized worker agents: stock_picker, order_execution, and technical_analysis. "
            "You can also execute operations directly using the Zerodha Kite MCP server. "
            "Your highest priority is capital preservation, followed by consistency, followed by profitability. "
            "Maintain strategic reserve capital (war chest) at all times. "
            "Avoid over-concentration. "
            "Do not engage in prediction-based forecasting, only analysis based on price-action and risk assessment. "  
            "Protect flexibility by preserving reserve cash during uncertain or defensive environments. "
            "Avoid prediction-based reasoning. Operate using confirmation-based logic only. "
            "Reject impulsive, emotional, extended, statistically weak, or structurally compromised setups. "
            "Never guarantee outcomes. Always communicate probabilistically and conditionally. "
            "Always respond in a clear, concise, and professional manner. Do not repeat information already provided. "
            "Use DelegateTool to assign tasks to the appropriate worker agents when needed. "
            "If a user asks about a specific strategy, check if you have a relevant skill loaded. "
            "Ensure that you do not repeat messages or analysis that have already been communicated to the user."
        )
    )

    # Setup Tools
    tools = [
        Tool(
            name=TerminalTool.name,
            params={"no_change_timeout_seconds": 5},
        ),
        Tool(name=FileEditorTool.name),
        Tool(name="DelegateTool"),
    ]

    # MCP Configuration for Zerodha
    # NOTE: Ensure this block is indented at 4 spaces so it remains within the main() function body.
    MCP_CONFIG = {
        "mcpServers": {
            "ZerodhaKite": {
                "command": "npx",
                "args":["mcp-remote","https://mcp.kite.trade/mcp",], 
                "auth": "oauth", 
            }
        }
    }

    # Initialize Agent
    agent = Agent(llm=llm, 
                  condenser=condenser,
                  tools=tools, 
                  mcp_config=MCP_CONFIG, 
                  agent_context=agent_context)

    # Define a callback to handle displaying the agent's responses
    def conversation_callback(event: Event):
        if isinstance(event, LLMConvertibleEvent):
            msg = event.to_llm_message()
            # Only print messages from the assistant
            if msg.role == "assistant":
                if isinstance(msg.content, list):
                    for block in msg.content:
                        if block.type == "text":
                            print(f"\n[Agent]: {block.text}")
                elif isinstance(msg.content, str):
                    print(f"\n[Agent]: {msg.content}")

    # Initialize Conversation with a consistent ID to enable resumption
    cwd = f"{os.getcwd()}/workspace"
    conversation = Conversation(
        agent=agent, 
        persistence_dir="./history",
        conversation_id=CONSISTENT_ID,
        callbacks=[conversation_callback], 
        workspace=cwd,
        visualizer=DelegationVisualizer(name="Orchestrator")
    )

    print("=" * 60)
    print("Welcome to the Portfolio Manager Agent CLI!")
    print("Worker agents available: stock_picker, order_execution, technical_analysis.")
    print("Supported operations: login, get profile, get holdings, analyse portfolio, etc.")
    print("Type '/condense' to manually summarize history.")
    print("Type 'exit' or 'quit' to close the application.")
    print(f"Loaded {len(skills)} trading strategies as skills.")
    print("=" * 60)

    # Interactive loop
    while True:
        try:
            user_input = input("\n[You]: ").strip()
            # if not user_input:
            #     continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting Portfolio Manager Agent. Goodbye!")
                break
            
            if user_input.lower() == "/condense":
                print("Triggering manual condensation...")
                conversation.condense()
                print("Condensation successful!")
                continue
                
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
