#!/usr/bin/env python3
"""
Live Holdings & Account Synchronizer for Zerodha Kite MCP Server.
Maintains an active MCP session, requests login authorization link,
writes authorization link to workspace/login_info.json,
polls for browser authorization completion, and fetches live holdings,
positions, and profile data into workspace/.
"""

import os
import sys
import json
import asyncio

async def main():
    os.makedirs("workspace", exist_ok=True)
    try:
        from mcp.client.stdio import stdio_client, StdioServerParameters
        from mcp import ClientSession

        params = StdioServerParameters(command="npx", args=["-y", "mcp-remote", "https://mcp.kite.trade/mcp"])
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("Requesting login URL from Zerodha Kite MCP Server...", flush=True)
                login_res = await session.call_tool("login", {})
                login_text = ""
                for c in login_res.content:
                    if hasattr(c, "text"):
                        login_text += c.text
                
                # Write login URL info for agent to read immediately
                with open("workspace/login_info.json", "w") as f:
                    json.dump({
                        "status": "pending",
                        "mcp_text": login_text
                    }, f, indent=2)
                
                print("Login info written to workspace/login_info.json. Polling for authorization...", flush=True)

                for attempt in range(60): # Poll up to 3 minutes (180s)
                    await asyncio.sleep(3)
                    profile_res = await session.call_tool("get_profile", {})
                    is_err = getattr(profile_res, "isError", False)
                    prof_text = "".join([c.text for c in profile_res.content if hasattr(c, "text")])

                    if not is_err and "Please log in" not in prof_text and "error" not in prof_text.lower():
                        print(f"\n✅ Authorization confirmed! Synchronizing account data...", flush=True)
                        
                        # 1. Fetch Profile
                        try:
                            profile_data = json.loads(prof_text)
                            with open("workspace/live_profile.json", "w") as f:
                                json.dump(profile_data, f, indent=2)
                        except Exception:
                            with open("workspace/live_profile.raw.txt", "w") as f:
                                f.write(prof_text)

                        # 2. Fetch Holdings
                        holdings_res = await session.call_tool("get_holdings", {})
                        holdings_text = "".join([c.text for c in holdings_res.content if hasattr(c, "text")])
                        try:
                            holdings_data = json.loads(holdings_text)
                            with open("workspace/live_holdings.json", "w") as f:
                                json.dump(holdings_data, f, indent=2)
                            print(f"Saved live holdings ({len(holdings_data)} items) to workspace/live_holdings.json", flush=True)
                        except Exception:
                            with open("workspace/live_holdings.raw.txt", "w") as f:
                                f.write(holdings_text)

                        # 3. Fetch Positions
                        positions_res = await session.call_tool("get_positions", {})
                        positions_text = "".join([c.text for c in positions_res.content if hasattr(c, "text")])
                        try:
                            pos_data = json.loads(positions_text)
                            with open("workspace/live_positions.json", "w") as f:
                                json.dump(pos_data, f, indent=2)
                        except Exception:
                            with open("workspace/live_positions.raw.txt", "w") as f:
                                f.write(positions_text)

                        # Status update
                        with open("workspace/login_info.json", "w") as f:
                            json.dump({
                                "status": "authenticated",
                                "holdings_count": len(holdings_data) if isinstance(holdings_data, list) else 0
                            }, f, indent=2)
                        
                        return
                
                print("\nTimed out waiting for authorization.", flush=True)
                with open("workspace/login_info.json", "w") as f:
                    json.dump({"status": "timeout"}, f, indent=2)

    except Exception as e:
        print(f"Error in sync process: {e}", flush=True)
        with open("workspace/login_info.json", "w") as f:
            json.dump({"status": "error", "error": str(e)}, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
