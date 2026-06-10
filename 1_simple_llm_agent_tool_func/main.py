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