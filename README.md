# Reddit-News-Agent-System-Using-MCP-and-ADK

In this project multiple agents are created to fetch news from Reddit's subreddits baswd on user's query in natural language, summarized in the newscaster format and the final summarized news is returned to the user. Multimodality is also integrated in this project wehre, user can hear the summarized news in English instead of just reading the text information. This project is built using Google's **Agent Development Kit** which was recently released for building agents from scratch and for easy deployement and for production and, using **Model Context Protocol** released by Anthropic recently for effective communication within agents and between multiple tools and agents.

# General Setup
Clone the repository:

git clone https://github.com/RishabhMathur06/Reddit-News-Agent-System-Using-MCP-and-ADK
cd agents

# Create and activate a virtual environment (Recommended):

python -m venv .venv
# On Windows
.\.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# Install general dependencies:

pip install -r requirements.txt
Agent-Specific Setup: Navigate to the specific agent's directory within agents/ and follow the instructions in its README.md (or follow the steps below for the default agent).

Setup & Running Agents
Navigate to Agent Directory:

cd agents/reddit_scout
Set up API Key:

Copy the example environment file:
cp ../.env.example .env
Edit the .env file and add your Google AI API Key. You can obtain one from Google AI Studio.
GOOGLE_API_KEY=YOUR_API_KEY_HERE
Note: You might need to load this into your environment depending on your OS and shell (source .env or similar) if python-dotenv doesn't automatically pick it up when running adk.
Run the Agent:

Make sure your virtual environment (from the root directory) is activated.
From the agents/reddit_scout directory, run the agent using the ADK CLI, specifying the core code package:
adk run reddit_scout
Alternatively, from the project root (adk-made-simple), you might be able to run:
adk run agents/reddit_scout
(Check ADK documentation for preferred discovery method)
Asynchronous agents can only be run from the web view, so first cd into the agents directory and run
adk web
(Check ADK documentation for preferred discovery method)
Interact: The agent will start, and you can interact with it in the terminal. Try prompts like:

What's the latest news?
Give me news from unrealengine
Project Structure Overview
adk-made-simple/
├── agents/
│   ├── reddit_scout/        # Lesson 1: Reddit Scout Agent
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── async_reddit_scout/  # Lesson 2: Asynchronous Reddit Scout Agent
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── summarizer/          # Lesson 2: Newscaster Summarizer Agent
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── speaker/             # Lesson 2: Speaker Agent
│   │   ├── __init__.py
│   │   └── agent.py
│   └── coordinator/         # Lesson 2: Coordinator Agent combining sub-agents
│       ├── __init__.py
│       └── agent.py
├── .env.example             # Environment variables example
├── .gitignore               # Root gitignore file
├── requirements.txt         # Project dependencies
├── README.md                # This file (Overall Project 
