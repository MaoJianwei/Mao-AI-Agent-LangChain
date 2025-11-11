import asyncio

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

async def main():

    llm = ChatOpenAI(
        model="glm-4.5-flash",
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        api_key="",
    )

    client = MultiServerMCPClient(
        {
            "maoCloud": {
                "transport": "streamable_http",  # HTTP-based remote server
                # Ensure you start your weather server on port 8000
                "url": "http://www.maojianwei.com:0/mcp/",
            }
        }
    )
    maoTools = await client.get_tools()
    maoTools.append(get_weather)

    agent = create_agent(
        model=llm,
        tools=maoTools,
        system_prompt="You are a helpful assistant",
    )

    # Run the agent
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": "集群中各个节点的状态如何，有没有问题？"}]},
        stream_mode=["updates", "messages"]
    ):
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())
