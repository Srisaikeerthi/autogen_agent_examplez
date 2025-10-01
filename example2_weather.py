import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()

# Define a simple weather tool
async def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is 35 C and Sunny."

async def main() -> None:
    # Create model client
    model_client = OpenAIChatCompletionClient(
       model="gpt-4o",
       api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create agent with tool capability
    agent = AssistantAgent(
        name="John",   # name of the agent 
        model_client=model_client,   # brain of the agent 
        tools=[get_weather],  # tools to the agent 
        system_message="""You are a helpful weather assistant. You are a
         helpful weather assistant.You are a helpful weather assistant. 
         You are a helpful weather assistant.You are a helpful weather 
         assistant.""",   # roles of the agent
        model_client_stream=True,  # should the response be a stream?
    )
    
    # Run the agent with streaming output
    response = agent.run_stream(task="What is the weather in New York?")
    await Console(response)
    
    # Close the client
    await model_client.close()

asyncio.run(main())
