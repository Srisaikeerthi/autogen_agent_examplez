import asyncio
from autogen_agentchat.agents import AssistantAgent
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
    
    # Create two agents with different roles
    teacher = AssistantAgent(
        name="teacher",
        model_client=model_client,
        system_message="You are a math teacher. Explain concepts clearly and ask follow-up questions.",
    )
    
    student = AssistantAgent(
        name="student", 
        model_client=model_client,
        system_message="You are an eager student learning math. Ask questions when confused.",
    )
    
    # Start conversation from teacher's perspective
    result = await teacher.run(task="Explain what a derivative is to a beginner")
    print("Teacher:", result.messages[-1].content)
    
    # Student responds to teacher
    student_result = await student.run(task=f"The teacher said: {result.messages[-1].content}. Please ask a clarifying question about derivatives.")
    print("Student:", student_result.messages[-1].content)
    
    await model_client.close()

asyncio.run(main())
