"""
Demo 1: Simple LLM Agent with Tool Function
============================================

This script demonstrates the fundamentals of LangChain agents with basic tool integration.
It creates an AI agent that can fetch real-time weather information and respond to user queries.

KEY CONCEPTS:
  - LLM Agent: An AI that can reason about goals and use tools to achieve them
  - Tools: Custom functions that extend agent capabilities (weather lookup)
  - Tool Decoration: Using @tool decorator to expose functions to the agent
  - Single-turn Conversation: One question/answer cycle

FEATURES:
  ✓ Simple tool integration with automatic type inference
  ✓ Google Gemini LLM for agent reasoning (gemini-2.5-flash-lite)
  ✓ Real-world API integration (wttr.in for weather data)
  ✓ Natural language interaction
  ✓ Minimal setup - beginner friendly

REQUIREMENTS:
  - GOOGLE_API_KEY environment variable set in .env file
  - Internet connection for weather API calls
  - Dependencies: langchain, langchain-google-genai, requests, python-dotenv

USAGE:
  $ python 1_simple_llm_agent_tool_func/main.py

EXPECTED OUTPUT:
  Natural language response about weather in San Francisco, e.g.:
  "The weather in San Francisco is currently [weather description]"

NOTES:
  - This is a foundation for understanding LangChain agents
  - See Demo 2 for advanced features like context management and structured outputs
  - Weather API (wttr.in) has rate limiting (~10 requests/min per IP)
"""

import requests
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage

load_dotenv()

@tool("get_weather", description="Return weather information for a given city", return_direct=False)
def get_weather(city: str):
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    response.raise_for_status()
    return response.json()

agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)

result = agent.invoke({
    "messages": [
        HumanMessage(content="What is the weather in San Francisco?")
    ]
})

print(result["messages"][-1].content)