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
        system_message="""You are a math teacher. Explain concepts clearly and 
        ask follow-up questions. """,
        model_client_stream=True,
    )
    
    student = AssistantAgent(
        name="student", 
        model_client=model_client,
        system_message="""You are an eager student learning math. 
        Ask questions when confused.""",
        model_client_stream=True,
    )

    # Start conversation from teacher's perspective
    teacher_result = await teacher.run(task="Explain what a probability is to a beginner")
    print("========Teacher:========", teacher_result.messages[-1].content)

    # Student responds to teacher
    student_result = await student.run(task=f"""The teacher said: 
    {teacher_result.messages[-1].content}.
     Please ask a clarifying question about probabilities.""")
    print("=========Student:===========", student_result.messages[-1].content)

    # Teacher answers student's question
    teacher_result = await teacher.run(task=f"""The student asked:
    {student_result.messages[-1].content}.
     Please provide a detailed answer.""")
    print("========Teacher:========", teacher_result.messages[-1].content)

    await model_client.close()

asyncio.run(main())
