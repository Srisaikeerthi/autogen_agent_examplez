import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from pydantic import BaseModel
from typing import List, Literal
import os
from dotenv import load_dotenv

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

class BookAnalysis(BaseModel):
    title: str
    author: str
    themes: List[str]
    difficulty_level: Literal["beginner", "intermediate", "advanced"]
    page_estimate: int
    key_takeaways: List[str]
    target_audience: str

async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Movie review agent
    movie_critic = AssistantAgent(
        name="movie_critic",
        model_client=model_client,
        system_message="You are a professional movie critic. Analyze movies thoroughly and provide structured reviews.",
        output_content_type=MovieReview,
    )
    
    # Book analysis agent  
    book_analyst = AssistantAgent(
        name="book_analyst", 
        model_client=model_client,
        system_message="You are a literary analyst. Provide comprehensive book analyses in structured format.",
        output_content_type=BookAnalysis,
    )
    
    # Test movie review
    print("=== MOVIE REVIEW ===")
    movie_result = await movie_critic.run(task="Review the movie 'Inception' directed by Christopher Nolan")
    
    if isinstance(movie_result.messages[-1], StructuredMessage):
        review = movie_result.messages[-1].content
        print(f"Title: {review.title}")
        print(f"Genre: {', '.join(review.genre)}")
        print(f"Rating: {review.rating}/10")
        print(f"Sentiment: {review.sentiment}")
        print(f"Summary: {review.summary}")
        print(f"Pros: {', '.join(review.pros)}")
        print(f"Cons: {', '.join(review.cons)}")
        print(f"Recommendation: {review.recommendation}")
    
    print("\n=== BOOK ANALYSIS ===")
    book_result = await book_analyst.run(task="Analyze the book 'The Hitchhiker's Guide to the Galaxy' by Douglas Adams")
    
    if isinstance(book_result.messages[-1], StructuredMessage):
        analysis = book_result.messages[-1].content
        print(f"Title: {analysis.title}")
        print(f"Author: {analysis.author}")
        print(f"Themes: {', '.join(analysis.themes)}")
        print(f"Difficulty: {analysis.difficulty_level}")
        print(f"Estimated Pages: {analysis.page_estimate}")
        print(f"Key Takeaways: {', '.join(analysis.key_takeaways)}")
        print(f"Target Audience: {analysis.target_audience}")
    
    await model_client.close()

asyncio.run(main())
