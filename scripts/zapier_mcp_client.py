#!/usr/bin/env python3
"""
Zapier MCP Client - Connect to Zapier MCP server and list available tools
"""
import asyncio
import json
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    token = "M2EwZDk5NTgtMmM3Ni00MmQ2LThmNzctMzJiYTI4N2Q1YjZiOm00UFFaVXJraEVVcEpOOXNvVGdnaVplMmZGVDduOHdCeVd1UGgzK0VHV3c9"
    url = f"https://mcp.zapier.com/api/v1/connect?token={token}"
    
    print(f"Connecting to Zapier MCP at {url}...")
    print()
    
    try:
        async with sse_client(url) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                
                # List available tools
                tools = await session.list_tools()
                
                print(f"✅ Connected! Found {len(tools.tools)} tools:\n")
                
                for i, tool in enumerate(tools.tools[:20], 1):  # Show first 20
                    print(f"{i}. {tool.name}")
                    if tool.description:
                        print(f"   └─ {tool.description[:100]}")
                    print()
                
                if len(tools.tools) > 20:
                    print(f"... and {len(tools.tools) - 20} more tools")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
