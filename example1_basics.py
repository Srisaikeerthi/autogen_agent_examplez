import asyncio
# pip install -U "autogen-agentchat" "autogen-ext[openai]"
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv #pip install python-dotenv

load_dotenv()

openai_api_key=os.getenv("OPENAI_API_KEY")

async def main() -> None:

    # Create a model client
    model_client = OpenAIChatCompletionClient(
       model="gpt-4o",
       api_key=openai_api_key
    )

    # Create an assistant agent
    agent = AssistantAgent("assistant", model_client=model_client)

    # Run a simple task
    response = await agent.run(task="Say 'Hello World!'")
    print(response);
    
    print("=========RESPONSE RECEIVED FROM MODEL=========") # this will print after the model response is received
    
    # Close the client connection
    await model_client.close()

# Run the async function
asyncio.run(main())
