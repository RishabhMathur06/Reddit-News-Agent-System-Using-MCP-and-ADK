# Reddit-News-Agent-System-Using-MCP-and-ADK

In this project multiple agents are created to fetch news from Reddit's subreddits baswd on user's query in natural language, summarized in the newscaster format and the final summarized news is returned to the user. Multimodality is also integrated in this project wehre, user can hear the summarized news in English instead of just reading the text information. This project is built using Google's **Agent Development Kit** which was recently released for building agents from scratch and for easy deployement and for production and, using **Model Context Protocol** released by Anthropic recently for effective communication within agents and between multiple tools and agents.

## Agents

- **Reddit Scout**: Simulates fetching recent discussion titles from game development subreddits.
- **Summarizer**:
- **Text-to-Speech**:

## General Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/RishabhMathur06/Reddit-News-Agent-System-Using-MCP-and-ADK
    cd agents
    ```

2.  **Create and activate a virtual environment (Recommended):**

    ```bash
    python -m venv .venv
    # On Windows
    .\.venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install general dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Agent-Specific Setup:** Navigate to the specific agent's directory within `agents/` and follow the instructions in its `README.md` (or follow the steps below for the default agent).

## Setup & Running Agents

1.  **Navigate to Agent Directory:**

    ```bash
    cd agents/reddit_scout
    ```

2.  **Set up API Key:**

    - Copy the example environment file:
      ```bash
      cp ../.env.example .env
      ```
    - Edit the `.env` file and add your GoogleAI API Key, Reddit Credentials and Elevenlabs API Key.
      ```dotenv
      GOOGLE_GENAI_USE_VERTEXAI="False"
      GOOGLE_API_KEY="<Gemini API Key>"
    
      REDDIT_CLIENT_ID="<Reddit Client ID>"
      REDDIT_CLIENT_SECRET="<Reddit Client Secret Key>"
      REDDIT_USER_AGENT="GameDevNewsScout/0.1 by <your user-id>" # This can be configured. 
    
      ELEVENLABS_API_KEY="<Elevenlabs API Key>"
      ```
    - _Note:_ You might need to load this into your environment depending on your OS and shell (`source .env` or similar) if `python-dotenv` doesn't automatically pick it up when running `adk`.

3.  **Run the Agent:**

    - Make sure your virtual environment (from the root directory) is activated.
    - From the `agents/reddit_scout` directory, run the agent using the ADK CLI, specifying the core code package:
      ```bash
      adk run aync_reddit_scout
      ```
    - Alternatively, from the project root (`Reddit-News-Agent-System-Using-MCP-and-ADK`), you might be able to run:
      ```bash
      adk run agents/async_reddit_scout
      ```
      _(Check ADK documentation for preferred discovery method)_
    - Asynchronous agents can only be run from the web view, so first `cd` into the `agents` directory and run 
      ```bash
      adk web
      ```
      _(Check ADK documentation for preferred discovery method)_

4.  **Interact:** The agent will start, and you can interact with it in the terminal. Try prompts like:
    - `What's the latest news?`
    - `Give me news from unrealengine`
    - `Summarize the whole information`
    - `Convert this whole news to speech`

## Project Structure Overview

```
Reddit News Agent MCP ADK/
├── agents/
│   ├── reddit_scout/        
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── async_reddit_scout/  
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── summarizer/          
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── speaker/             
│   │   ├── __init__.py
│   │   └── agent.py
│   └── coordinator/         
│       ├── __init__.py
│       └── agent.py
├── .env                     # Environment variables example
├── .gitignore               # Root gitignore file
├── requirements.txt         # Project dependencies
└── README.md                # This file (Overall Project README)
```
