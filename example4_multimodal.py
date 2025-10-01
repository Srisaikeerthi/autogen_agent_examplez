import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import Image
import PIL
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",  # Make sure to use a vision-capable model
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create an agent that can handle images
    vision_agent = AssistantAgent(
        name="vision_assistant",
        model_client=model_client,
        system_message="You are an expert at describing and analyzing images in detail.",
    )
    
    # Load an image from the web
    image_response = requests.get("https://picsum.photos/400/300")
    pil_image = PIL.Image.open(BytesIO(image_response.content))
    img = Image(pil_image)
    
    # Create a multi-modal message
    multi_modal_message = MultiModalMessage(
        content=["Describe this image in detail and tell me what mood it conveys.", img], 
        source="user"
    )
    
    # Run the agent with the image
    result = await vision_agent.run(task=multi_modal_message)
    print("Vision Analysis:", result.messages[-1].content)
    
    await model_client.close()

asyncio.run(main())
