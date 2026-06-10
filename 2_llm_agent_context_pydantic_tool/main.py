"""
Demo 2: Advanced LLM Agent with Context & Pydantic-Style Tools
===============================================================

This script demonstrates advanced LangChain features including user context, structured
responses, context-aware tools, and conversation memory management. This is a production-
ready pattern for building intelligent agents.

KEY CONCEPTS:
  - Context Schema: User-specific data passed to tools (user_id, preferences, etc.)
  - ToolRuntime: Special tool parameter that receives access to agent context
  - Response Format: Pydantic-style dataclass with structured fields and descriptions
  - Checkpointer: Memory persistence for multi-turn conversations
  - Thread ID: Unique identifier for conversation sessions
  - Model Temperature: Controls randomness (0.3 = more deterministic)

FEATURES:
  ✓ Context-aware tools that access user information
  ✓ Structured output with type-safe Pydantic dataclasses
  ✓ Conversation memory using InMemorySaver checkpointer
  ✓ Multi-turn conversation support (thread_id based)
  ✓ Field metadata guidance for LLM output formatting
  ✓ Deterministic responses with lower temperature setting
  ✓ Two tools working together (locate_user + get_weather)

ARCHITECTURE:
  Context (user_id)
    ↓
  Agent with Tools
    ├─ locate_user(runtime: ToolRuntime[Context])
    │   └─ Looks up city based on user_id from context
    └─ get_weather(city: str)
        └─ Fetches weather from wttr.in API
    ↓
  ResponseFormat (structured output)
    ├─ summary: Natural language weather description
    ├─ temperature_celsius: Numeric value
    ├─ temperature_fahrenheit: Numeric value
    └─ humidity: Numeric value

REQUIREMENTS:
  - GOOGLE_API_KEY environment variable set in .env file
  - Internet connection for weather API calls
  - Dependencies: langchain, langchain-google-genai, langgraph, requests, python-dotenv

USAGE:
  $ python 2_llm_agent_context_pydantic_tool/main.py

EXPECTED OUTPUT:
  Structured response object with:
    - summary: "Heavy rain and windy"
    - temperature_celsius: 12.0
    - temperature_fahrenheit: 53.6
    - humidity: 88.0

"""

from dataclasses import dataclass, field

import requests
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

@dataclass
class Context:
    """Context containing user related core values"""
    user_id: str = field(
        metadata={"description": "The unique alphanumeric identifier for the user"}
    )

@dataclass
class ResponseFormat:
    summary: str = field(
        metadata={"description": "Short and precise string summary of weather information"}
    )
    temperature_celsius: float = field(
        metadata={"description": "Numeric temperature in celsius one place decimal"}
    )
    temperature_fahrenheit: float = field(
        metadata={"description": "Numeric temperature fahrenheit in one place decimal"}
    )
    humidity: float = field(
        metadata={"description": "Numeric humidity value in one place decimal"}
    )

@tool('locate_user', description="Look up a user's city based on the context")
def locate_user(runtime: ToolRuntime[Context]):
    match runtime.context.user_id:
        case 'ABC123':
            return 'Vienna'
        case 'XYZ456':
            return 'London'
        case 'HJKL111':
            return 'Paris'
        case _:
            return 'Unknown'

@tool("get_weather", description="Return weather information for a given city", return_direct=False)
def get_weather(city: str):
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    response.raise_for_status()
    return response.json()

model = init_chat_model('google_genai:gemini-2.5-flash-lite', temperature=0.3)

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[get_weather, locate_user],
    system_prompt="You are a helpful weather assistant",
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

config = {'configurable': {'thread_id': '1'}}

result = agent.invoke({
    'messages': [
        HumanMessage(content="What is the weather like?")
    ]},
    config=config,
    context=Context(user_id='ABC123')
)

print(result["structured_response"])
print(result["structured_response"].summary)
print(result["structured_response"].temperature_celsius)