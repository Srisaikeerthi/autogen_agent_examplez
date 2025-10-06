# this version uses Google Gemini 2.5 Pro model
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from pydantic import BaseModel
from typing import List, Literal
import os
from dotenv import load_dotenv
from autogen_core.models import ModelInfo

load_dotenv()

# Define structured output models
class MovieReview(BaseModel):
    title: str
    genre: List[str]
    rating: int  # 1-10 scale
    sentiment: Literal["positive", "negative", "mixed"]
    summary: str
    pros: List[str]
    cons: List[str]
    recommendation: str

async def main() -> None:
    # we are using OpenAI client for Google Gemini 2.5 Pro -- because it is OpenAI Compatible
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        # the following is needed as Google Gemini 2.5 Pro is not in the default model list
        model_info=ModelInfo(vision=True, function_calling=True, json_output=True, 
        family="unknown", structured_output=True),
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Movie review agent
    movie_critic_agent = AssistantAgent(
        name="movie_critic",
        model_client=model_client,
        system_message="""You are a professional movie critic. 
        Analyze movies thoroughly and provide structured reviews.""",
        output_content_type=MovieReview, # structured output
    )
    
    # Test movie review
    print("=== MOVIE REVIEW ===")
    movie_result = await movie_critic_agent.run(task="""Review the movie 
    'Inception'""")

    if isinstance(movie_result.messages[-1], StructuredMessage):
        review = movie_result.messages[-1].content
        print(f"=====Title=====: {review.title}")
        print(f"=====Genre=====: {', '.join(review.genre)}")
        print(f"=====Rating=====: {review.rating}/10")
        print(f"=====Sentiment=====: {review.sentiment}")
        print(f"=====Summary=====: {review.summary}")
        print(f"=====Pros=====: {', '.join(review.pros)}")
        print(f"=====Cons=====: {', '.join(review.cons)}")
        print(f"=====Recommendation=====: {review.recommendation}")

    await model_client.close()

asyncio.run(main())
