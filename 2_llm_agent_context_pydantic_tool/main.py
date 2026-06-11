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
import json

import requests
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

# google_genai:gemini-2.5-flash-lite
model_name = 'qwen2.5:latest'


@dataclass
class Context:
    """Context containing user related core values"""
    user_id: str = field(
        metadata={"description": "The unique alphanumeric identifier for the user"}
    )


@dataclass
class ResponseFormat:
    """Response format or structure of the weather API"""
    summary: str = field(
        metadata={"description": "String summary of weather information"}
    )
    temperature_celsius: float = field(
        metadata={"description": "Numeric temperature in celsius one place decimal"}
    )
    temperature_fahrenheit: float = field(
        metadata={"description": "Numeric temperature fahrenheit in one place decimal"}
    )
    humidity: float = field(metadata={"description": "Numeric humidity value in one place decimal"})


@tool("get_weather", description="Return weather information for a given city", return_direct=False)
def get_weather(city: str):
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    response.raise_for_status()
    return response.json()


model = init_chat_model(model_name, model_provider="ollama", temperature=0.3)

checkpointer = InMemorySaver()

# Create user context for the session
user_context = Context(user_id="ABC123")

# Define a wrapper for locate_user that includes the context
@tool("locate_user", description="Look up a user's city based on the context")
def locate_user_wrapper():
    """Returns the user's city based on their user_id"""
    match user_context.user_id:
        case "ABC123":
            return "Vienna"
        case "XYZ456":
            return "London"
        case "HJKL111":
            return "Paris"
        case _:
            return "Unknown"

agent = create_agent(
    model=model,
    tools=[get_weather, locate_user_wrapper],
    system_prompt="""You are a helpful weather assistant.
Your job is to:
1. First call locate_user() to get the user's city
2. Then call get_weather() with that city
3. Format your response as JSON with these fields:
   - summary: Natural language weather description
   - temperature_celsius: Temperature in Celsius (one decimal place)
   - temperature_fahrenheit: Temperature in Fahrenheit (one decimal place)
   - humidity: Humidity percentage (one decimal place)

Return the response as valid JSON.""",
    checkpointer=checkpointer,
)

config = {"configurable": {"thread_id": "1"}}

result = agent.invoke(
    {"messages": [HumanMessage(content="What is the weather like?")]},
    config=config,
)

# Extract the final AI response
final_message = result["messages"][-1].content

print("\n📝 Raw Response from Agent:")
print(final_message)

# Better JSON extraction that handles nested objects
def extract_json(text):
    """Extract JSON object from text"""
    # Try to find a JSON object
    start = text.find('{')
    if start == -1:
        return None

    # Find the matching closing brace
    depth = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    return None

json_str = extract_json(final_message)
if json_str:
    try:
        weather_data = json.loads(json_str)
        # Convert to ResponseFormat dataclass
        response = ResponseFormat(
            summary=weather_data.get("summary", ""),
            temperature_celsius=float(weather_data.get("temperature_celsius", 0)),
            temperature_fahrenheit=float(weather_data.get("temperature_fahrenheit", 0)),
            humidity=float(weather_data.get("humidity", 0)),
        )
        print("\n✅ Structured Response:")
        print(f"Summary: {response.summary}")
        print(f"Temperature (°C): {response.temperature_celsius}")
        print(f"Temperature (°F): {response.temperature_fahrenheit}")
        print(f"Humidity: {response.humidity}%")
    except json.JSONDecodeError as e:
        print(f"\n⚠️  Could not parse JSON: {e}")
        print(f"Raw response: {final_message}")
else:
    print("\n⚠️  No JSON found in response")
    print(f"Raw response: {final_message}")
