from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import os

load_dotenv()

async def create_summarizer_agent():
    # Adjustable, any model could be used.
    llm = LiteLlm(model="gemini/gemini-2.5-flash-preview-04-17", api_key=os.environ.get("GOOGLE_API_KEY"))

    summarizer = Agent(
        name="newscaster_summarizer_agent",
        description="Summarizes a list of Reddit post titles in a newscaster style.",
        model=llm,
        instruction=(
            "You are a news anchor summarizing Reddit headlines. "
            "Given a list of post titles, provide a concise, engaging summary in a professional newscaster style. "
            "Highlight key themes or interesting points found only in the titles. "
            "Start with an anchor intro like 'Here are today's top stories from the subreddit...' or similar. Keep it brief."
            "Refer to subreddits by name, no need to mention 'r/'."
        )
    )

    return summarizer

# Exposing root agent for ADK
root_agent = create_summarizer_agent()