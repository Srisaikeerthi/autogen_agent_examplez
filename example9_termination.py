import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()

async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create primary content creator agent
    writer_agent = AssistantAgent(
        "writer",
        model_client=model_client,
        system_message="""You are a creative writer.
         Write engaging content based on requests and improve it based on feedback.""",
    )
    
    # Create critic agent for feedback
    critic_agent = AssistantAgent(
        "critic",
        model_client=model_client,
        system_message="""You are a content editor.
        Provide constructive feedback on writing. 
        You must give at least one feedback and get it improved before approving. 
        Respond with 'APPROVED' when the content meets high standards."""
    )
    
    # Define termination condition
    termination = TextMentionTermination("APPROVED")
    
    # Create team with round-robin pattern
    team = RoundRobinGroupChat([writer_agent, critic_agent], 
    termination_condition=termination)
    
    # Run the team
    print("=== REFLECTION PATTERN EXAMPLE ===")
    await Console(team.run_stream(task="""Write a compelling product description 
    for a smart fitness watch"""))
    
    await model_client.close()

asyncio.run(main())
