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
    system_prompt="You are a helpful weather assistant, who are always cracks jokes"
    " and humorous while remaining helpful.",
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

config = {'configurable': {'thread_id': 1}}

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