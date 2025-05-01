# Importing dependencies.
import random
import os
from .utils import load_instruction_from_file
from google.adk.agents import Agent
import praw
from praw.exceptions import PRAWException
from dotenv import load_dotenv

# Loading .env file which contains the configurations
load_dotenv()

# The actual function for fetching reddit posts.
def get_reddit_gamedev_news(subreddit: str, limit: int = 5) -> dict[str, list[str]]:
    """
    Fetches top post titles from specified subreddits using the Reddit API.

    Args:
        subreddit: The names of the subreddits to fetch news from (e.g., 'gamedev', 'Unity3D', etc.).
        limit: The maximum number of top posts to fetch.

    Returns:
        A dictionary with the subreddits names as key and a list of
        post titles as value. Returns an error message if credentials are
        missing, the subreddit is invalid, or an API error occurs specifying error in detail.
    """

    print(f"--- Tool called: Fetching from r/{subreddit} via Reddit API ---")

    # Setting Reddit Credentials by importing them from .env file.
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    # If all credentials are not present for reddit, give error.
    if not all([client_id, client_secret, user_agent]):
        print("--- Tool error: Reddit API credentials missing in .env file. ---")
        return {subreddit: ["Error: Reddit API credentials not configured."]}

    try:
        # PRAW -> Python Reddit API Wrapper.
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

        # Check if subreddit exists and is accessible
        reddit.subreddits.search_by_name(subreddit, exact=True)
        sub = reddit.subreddit(subreddit)
        top_posts = list(sub.hot(limit=limit)) # Fetch hot posts
        titles = [post.title for post in top_posts]

        if not titles:
             return {subreddit: [f"No recent hot posts found in r/{subreddit}."]}
        return {subreddit: titles}
    
    except PRAWException as e:
        print(f"--- Tool error: Reddit API error for r/{subreddit}: {e} ---")
        # More specific error handling could be added here (e.g., 404 for invalid sub)
        return {subreddit: [f"Error accessing r/{subreddit}. It might be private, banned, or non-existent. Details: {e}"]}
    
    except Exception as e: # Catch other potential errors
        print(f"--- Tool error: Unexpected error for r/{subreddit}: {e} ---")
        return {subreddit: [f"An unexpected error occurred while fetching from r/{subreddit}."]}
    
# Creating a fake Reddit API call for demonstration purposes.
def get_mock_reddit_gamedev_news(subreddit: str) -> dict[str, list[str]]:
    """
    Simulates fetching top post titles from a game development subreddit.

    Args:
        subreddit: The name of the subreddit to fetch news from (e.g., 'gamedev').

    Returns:
        A dictionary with the subreddit name as key and a list of
        mock post titles as value. Returns a message if the subreddit is unknown.
    """

    print(f"--- Tool called: Simulating fetch from r/{subreddit} ---")

    mock_titles: dict[str, list[str]] = {
        "gamedev": [
            "Show HN: My new procedural level generator using Rust",
            "Unity releases update 2023.3 LTS - Key features discussion",
            "Best practices for optimizing physics in networked multiplayer games",
            "Debate: Is ECS the future for all game engines? Performance comparison.",
            "Looking for constructive feedback on my indie game's pixel art style",
            "How to get started with Godot 4.2 GDScript",
            "Unreal Engine 5.4 Nanite & Lumen deep dive",
        ],
        "unrealengine": [
            "Unreal Engine 5.4 Performance Guide for large open worlds",
            "How to implement advanced Niagara particle effects for magic spells",
            "MetaHumans Animator tutorial: Lip sync and facial expressions",
            "Showcase: Sci-Fi cinematic created entirely in UE5",
            "Troubleshooting Lumen global illumination artifacts in indoor scenes",
            "Marketplace highlight: Advanced locomotion system",
            "Tips for migrating projects from UE4 to UE5",
        ],
        "unity3d": [
            "Best practices for mobile game optimization in Unity 2023 LTS",
            "Understanding Unity's Data-Oriented Technology Stack (DOTS) and Burst Compiler",
            "Tutorial: Creating custom PBR shaders with Unity Shader Graph",
            "Top free assets from the Unity Asset Store this month",
            "Migrating project from URP to HDRP - Common pitfalls and solutions",
            "Introduction to Unity Muse for texture generation",
            "Networking in Unity: Netcode for GameObjects vs Photon PUN",
        ]
    }
    
    # Normalize subreddit name for lookup
    normalized_subreddit = subreddit.lower()

    if normalized_subreddit in mock_titles:
        available_titles = mock_titles[normalized_subreddit]

        # Return a random subset to make it seem dynamic
        num_to_return = min(len(available_titles), 3) # Return up to 3 random titles

        selected_titles = random.sample(available_titles, num_to_return)

        return {subreddit: selected_titles}
    else:
        print(f"--- Tool warning: Unknown subreddit '{subreddit}' requested. ---")

        return {subreddit: [f"Sorry, I don't have mock data for r/{subreddit}."]}


# Defining the agent.
agent = Agent(
    name="reddit_scout_agent",
    description="A Reddit scout agent that searches for the most relevant posts in given subreddits.",
    model="gemini-1.5-flash-latest",
    instruction=load_instruction_from_file("reddit_instruction.txt"),
    tools=[get_reddit_gamedev_news]
)