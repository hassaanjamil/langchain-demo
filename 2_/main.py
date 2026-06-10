from dataclasses import dataclass

import requests
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

@dataclass
class Context:
    user_id: str

@dataclass
class ResponseFormat:
    summary: str
    temperature_celsius: float
    temperature_fahrenheit: float
    humidity: float

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
    system_prompt="You are a helpful weather assistant, who are always cracks jokes"
    " and humorous while remaining helpful.",
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

config = {'configurable': {'thread_id': 1}}

result = agent.invoke({
    'messages': [
        HumanMessage(content="What is the weather in San Francisco?")
    ],
    config=config
})

print(result["messages"][-1].content)