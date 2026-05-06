References:
agent-sdk-examples/25_agent_delegation.py

Main code:
src/portfolio_agent.py

Objective:
Update portfolio_agent to a multi-agent system.
Refer agent delegation example from agent-sdk-examples for guidance on implementing multi-agent system using agent-sdk
Prepare 3 worker agents, 1 orchestrator agent. Following are the personas for each agent:
Worker agents:
1. Stock picker: Find the high momentum stocks from the current market. 
    - Follow the market trend to decide on the approach
    - Fix expected profit
    - Fix stop loss
2. Order execution: Execute/place orders (GTT or any other type of order)
3. Technical analysis: Thoroough technical analysis on 

Orchestrator agent: the portfolio main agent