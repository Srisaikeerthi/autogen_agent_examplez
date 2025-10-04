# Sequential Workflow with Handoffs Example
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import HandoffTermination
from autogen_agentchat.teams import Handoffs
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
    
    # Define sequential workflow agents
    requirements_analyst = AssistantAgent(
        "requirements_analyst",
        model_client=model_client,
        system_message="You analyze requirements and create detailed specifications. End with 'HANDOFF_TO_ARCHITECT' when complete.",
    )
    
    architect = AssistantAgent(
        "architect", 
        model_client=model_client,
        system_message="You design system architecture based on requirements. End with 'HANDOFF_TO_DEVELOPER' when complete.",
    )
    
    developer = AssistantAgent(
        "developer",
        model_client=model_client,
        system_message="You create implementation plans based on architecture. End with 'DEVELOPMENT_COMPLETE' when finished.",
    )
    
    # Define handoff conditions
    handoff_to_architect = HandoffTermination(target="architect")
    handoff_to_developer = HandoffTermination(target="developer") 
    development_complete = HandoffTermination(target="COMPLETE")
    
    # Create sequential handoff workflow
    workflow = Handoffs([
        (requirements_analyst, handoff_to_architect),
        (architect, handoff_to_developer),
        (developer, development_complete)
    ])
    
    print("=== SEQUENTIAL WORKFLOW WITH HANDOFFS ===")
    await Console(workflow.run_stream(task="""Design and plan the implementation of a
    real-time chat application with user authentication and message history."""))

    await model_client.close()

asyncio.run(main())
