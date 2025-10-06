import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import StructuredMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo
from pydantic import BaseModel
from typing import List,Literal
import os
from dotenv import load_dotenv
 
load_dotenv()
 
class WriterAgentOutput(BaseModel):
    title : str
    story : str
    moral_story : str
 
# Create the Writer Agent tool function that generates a short story
async def writer_agent_tool(prompt: str) -> str:
    '''Writer agent that generates a short story based on the prompt.'''
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        model_info=ModelInfo(vision=True,function_calling=True,json_output=True,
                             family="unknown",structured_output=True),
        api_key=os.getenv('GOOGLE_API_KEY')
    )
 
    writer_agent = AssistantAgent(
        "writer_agent",
        model_client=model_client,
        system_message='''You are a creative writer. 
        Write a compelling and engaging short story based on the user prompt.''',
        output_content_type=WriterAgentOutput,
    )
 
    result = await writer_agent.run(task=f'Write a short story about: {prompt}')
    await model_client.close()
    return result.messages[-1].content
 
 
async def main() -> None:
    # Get user input for the story prompt
    user_prompt = input("Enter the title or theme for the short story: ")
 
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        model_info=ModelInfo(vision=True,function_calling=True,json_output=True,
                             family="unknown",structured_output=True),
        api_key=os.getenv('GOOGLE_API_KEY')
    )
 
    coordinator = AssistantAgent(
        "coordinator",
        model_client=model_client,
        tools=[writer_agent_tool],
        system_message='''You are a project coordinator. 
        When a task is given, delegate it to the appropriate agent and return the result.''',
        max_tool_iterations=3,
    )
 
    team = RoundRobinGroupChat(
        [coordinator],
        termination_condition=MaxMessageTermination(6)
    )
 
    print('\n=== AGENT-BASED WORKFLOW ===')
    result = await team.run(task=f'Write a short story about: {user_prompt}')
 
    print(f'\nStory generation completed with {len(result.messages)} messages')
    print("Coordinator Transcript:")
    for msg in result.messages:
        print(f"{msg.source}: {msg.content}\n")
    if isinstance(result.messages[-1],StructuredMessage):
        review = result.messages[-1].content
        print(f"====Title====: {review.title}")
        print(f"====Moral_story====: {review.moral_story}")
        print(f"====Story====: {review.story}")

    await model_client.close()
 
# Run the workflow
asyncio.run(main())