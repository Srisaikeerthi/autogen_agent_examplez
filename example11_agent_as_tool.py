import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()

# Create specialized agent functions that can be used as tools
async def research_agent_tool(query: str) -> str:
    """Research agent that provides market data and insights."""
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    research_agent = AssistantAgent(
        "research_specialist",
        model_client=model_client,
        system_message="You are a specialized research agent. Provide concise, factual research findings.",
    )
    
    result = await research_agent.run(task=f"Research this topic: {query}")
    await model_client.close()
    return result.messages[-1].content

async def calculator_agent_tool(expression: str) -> str:
    """Calculator agent that performs mathematical calculations."""
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o", 
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    calc_agent = AssistantAgent(
        "calculator",
        model_client=model_client,
        system_message="You are a precise calculator. Solve mathematical expressions and show your work.",
    )
    
    result = await calc_agent.run(task=f"Calculate: {expression}")
    await model_client.close()
    return result.messages[-1].content

async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create coordinator agent that uses other agents as tools
    coordinator = AssistantAgent(
        "coordinator",
        model_client=model_client,
        tools=[research_agent_tool, calculator_agent_tool],
        system_message="You are a project coordinator. Use the research and calculator tools to provide comprehensive analysis.",
        max_tool_iterations=5,
    )
    
    # Create reviewer agent
    reviewer = AssistantAgent(
        "reviewer",
        model_client=model_client,
        system_message="You are a project reviewer. Evaluate the coordinator's analysis and suggest improvements.",
    )
    
    # Create team
    team = RoundRobinGroupChat(
        [coordinator, reviewer],
        termination_condition=MaxMessageTermination(6)
    )
    
    print("=== AGENT-AS-TOOL PATTERN ===")
    result = await team.run(task="Analyze the ROI of investing $100,000 in a SaaS startup. Research the market and calculate potential returns.")
    
    print(f"\nFinal analysis completed with {len(result.messages)} messages");

    print("Conversation Transcript:")
    for msg in result.messages:
        print(f"{msg.source}: {msg.content}\n")
    
    await model_client.close()

asyncio.run(main())
