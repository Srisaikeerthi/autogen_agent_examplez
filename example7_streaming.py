import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()

async def creative_writing_agent() -> str:
    """Generate a creative story with streaming output."""
    return "Write a short science fiction story about a time traveler who discovers something unexpected about their past. Make it engaging and include dialogue."

async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create a creative writing agent with streaming
    writer = AssistantAgent(
        name="creative_writer",
        model_client=model_client,
        system_message="You are a creative writer specializing in science fiction. Write engaging stories with vivid descriptions and compelling characters.",
        model_client_stream=True,  # Enable token streaming
    )
    
    print("Starting creative writing session...\n")
    
    # Use Console to display streaming output
    await Console(
        writer.run_stream(task=await creative_writing_agent()),
        output_stats=True,  # Show token usage stats
    )
    
    await model_client.close()

asyncio.run(main())
