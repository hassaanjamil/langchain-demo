# LangChain Demo Project

A comprehensive demo project showcasing different capabilities and features of [LangChain](https://langchain.com/) and its ecosystem. This project demonstrates building AI agents with tool integration, context management, and structured outputs.

## 🎯 Project Overview

This project contains practical examples of LangChain agents that interact with external APIs and maintain conversation context. It explores key features like:

- **Tool Integration**: Creating and using custom tools with LangChain agents
- **Context Management**: Managing user context across conversations
- **Structured Responses**: Using Pydantic/dataclasses for type-safe outputs
- **Conversation Memory**: Persistent conversation state with checkpointers
- **Large Language Models**: Integration with Google's Gemini models

## 📋 Prerequisites

- **Python**: 3.10 or higher
- **Package Manager**: `pip`, `uv`, or your preferred Python package manager
- **API Keys**: `Google Gemini` OR `Groq Cloud` API key (required for running demos)

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone or navigate to the project directory
cd <user>/AI/langchain-demo-project

# Create a virtual environment (if not already created)
python3.10 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
# Using uv (if installed)
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

You can obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/) & [Groq Cloud](https://console.groq.com/keys).

### 4. Run a Demo

```bash
# Run Demo 1: Simple LLM Agent
python 1_simple_llm_agent_tool_func/main.py

# Run Demo 2: Advanced Agent with Context & Pydantic Tools
python 2_llm_agent_context_pydantic_tool/main.py
```

Or using `uv`:

```bash
uv run 1_simple_llm_agent_tool_func/main.py
uv run 2_llm_agent_context_pydantic_tool/main.py
```

## 📁 Project Structure

```
langchain-demo-project/
├── README.md                                    # This file
├── pyproject.toml                               # Project metadata & dependencies
├── 1_simple_llm_agent_tool_func/
│   └── main.py                                  # Demo 1: Basic agent with tool
├── 2_llm_agent_context_pydantic_tool/
│   └── main.py                                  # Demo 2: Advanced agent with context
└── .env                                         # Environment variables (not in repo)
```

## 📚 Demo Explanations

### Demo 1: Simple LLM Agent with Tool Function

**File**: `1_simple_llm_agent_tool_func/main.py`

#### Overview

This demo demonstrates the basics of creating an agent with a custom tool for fetching weather information.

#### Key Components

**Tool Definition**:

```python
@tool("get_weather", description="Return weather information for a given city")
def get_weather(city: str):
    # Fetches real weather data from wttr.in API
```

**Agent Creation**:

```python
agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)
```

**Usage**:

```python
result = agent.invoke({
    "messages": [
        HumanMessage(content="What is the weather in San Francisco?")
    ]
})
```

#### Features

- Simple tool with string parameter
- Direct API integration with wttr.in
- Basic agent with one system prompt
- Single-turn conversation

#### Output

The agent responds with weather information formatted naturally by the LLM.

---

### Demo 2: Advanced Agent with Context & Pydantic Tool

**File**: `2_llm_agent_context_pydantic_tool/main.py`

#### Overview

This demo showcases advanced features including user context, structured outputs, multi-turn conversations, and conversation memory.

#### Key Components

**Context Definition** (User data):

```python
@dataclass
class Context:
    user_id: str  # Unique user identifier
```

**Response Format** (Structured output):

```python
@dataclass
class ResponseFormat:
    summary: str                    # Natural language summary
    temperature_celsius: float      # Numeric temperature
    temperature_fahrenheit: float   # Alternate unit
    humidity: float                 # Humidity percentage
```

**Context-Aware Tool**:

```python
@tool('locate_user')
def locate_user(runtime: ToolRuntime[Context]):
    # Access user context to determine location
    match runtime.context.user_id:
        case 'ABC123':
            return 'Vienna'
        # ...
```

**Agent with Advanced Features**:

```python
agent = create_agent(
    model=model,
    tools=[get_weather, locate_user],
    system_prompt="You are a helpful weather assistant...",
    context_schema=Context,           # User context
    response_format=ResponseFormat,   # Structured output
    checkpointer=checkpointer         # Conversation memory
)
```

#### Features

- **User Context**: Tools can access user information via `ToolRuntime[Context]`
- **Structured Responses**: Type-safe outputs using dataclasses with field descriptions
- **Conversation Memory**: In-memory checkpointer for multi-turn conversations
- **Thread-based State**: Config with `thread_id` for maintaining conversation history
- **System Personality**: Humor and helpfulness in agent behavior
- **Type Safety**: Pydantic-style field descriptions for LLM guidance

#### Output

Returns structured data with typed fields:

```python
result["structured_response"]              # Full response object
result["structured_response"].summary      # Natural language summary
result["structured_response"].temperature_celsius  # Numeric value
```

---

## 🔧 Dependencies

### Core Dependencies

| Package                  | Version | Purpose                                       |
| ------------------------ | ------- | --------------------------------------------- |
| `langchain`              | ≥1.3.6  | Core LangChain framework                      |
| `langchain-google-genai` | ≥4.2.5  | Google Gemini integration                     |
| `python-dotenv`          | ≥1.2.2  | Environment variable management               |
| `streamlit`              | ≥1.57.0 | Web UI framework (optional, for future demos) |

### Additional Dependencies (Implicit)

- `langgraph`: For checkpointer and state management (dependency of langchain)
- `requests`: For HTTP API calls (used in demos)

See `pyproject.toml` for complete project metadata.

## 🔐 Security & Configuration

### Environment Variables

The project uses `.env` files for sensitive configuration:

```env
GOOGLE_API_KEY=your_key_here
```

**Note**: Never commit `.env` files to version control. The file is typically added to `.gitignore`.

### API Keys

- **Google Gemini API**: Required for all LLM operations
  - Free tier available: [Google AI Studio](https://aistudio.google.com/)
  - Usage limits apply to free tier

### External APIs

- **wttr.in**: Free weather API, no authentication required
  - Rate limit: ~10 requests per minute from a single IP

## 💡 Development Notes

### Tool Design Patterns

**Simple Tools** (Demo 1):

```python
@tool("tool_name", description="...")
def my_tool(param: str) -> dict:
    return {"result": "..."}
```

**Context-Aware Tools** (Demo 2):

```python
@tool("tool_name")
def my_tool(runtime: ToolRuntime[MyContext]) -> str:
    user_id = runtime.context.user_id
    return f"Result for {user_id}"
```

### Response Formatting

Use dataclasses with field metadata to guide the LLM:

```python
@dataclass
class MyResponse:
    field: type = field(
        metadata={"description": "What this field represents"}
    )
```

### Conversation State Management

- **Checkpointer**: Stores conversation history and state
- **Thread ID**: Groups related messages together
- **Context**: User-specific data passed per invocation

```python
config = {'configurable': {'thread_id': 1}}
result = agent.invoke(input, config=config, context=Context(...))
```

### Model Selection

The project uses `gemini-2.5-flash-lite` for:

- ✅ Fast inference
- ✅ Lower cost
- ✅ Sufficient for demonstrations

For production, consider:

- `gemini-2.0-pro` for complex tasks
- `gemini-2.5-flash` for balanced performance

## 🧪 Testing & Debugging

### Run with Verbose Output

Modify `main.py` to enable logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test API Connectivity

```bash
python -c "
import requests
response = requests.get('https://wttr.in/London?format=j1')
print(response.status_code)
"
```

### Verify LLM Setup

```bash
python -c "
from langchain.chat_models import init_chat_model
model = init_chat_model('google_genai:gemini-2.5-flash-lite')
result = model.invoke('Hello')
print(result.content)
"
```

## 📖 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [wttr.in API](https://wttr.in/)

## 🚦 Common Issues & Solutions

### Issue: "API key not found"

**Solution**: Ensure `.env` file exists in project root with `GOOGLE_API_KEY=your_key`

### Issue: "Connection error to wttr.in"

**Solution**: Check internet connection; wttr.in may have rate limits. Wait and retry.

### Issue: "ModuleNotFoundError"

**Solution**: Activate virtual environment and reinstall dependencies

```bash
source .venv/bin/activate
pip install -e .
```

### Issue: "Invalid model name"

**Solution**: Verify model string format: `google_genai:gemini-2.5-flash-lite`

## 🎓 Next Steps for Development

1. **Add Database Tools**: Create tools that interact with databases
2. **Implement Retrieval**: Add RAG (Retrieval-Augmented Generation) capabilities
3. **Build Web UI**: Use Streamlit to create interactive demos
4. **Add Error Handling**: Comprehensive error handling and logging
5. **Unit Tests**: Add pytest tests for tools and agents
6. **Custom Memory**: Implement persistent storage for conversation history

## 📝 License

This project is a demonstration project. See LICENSE file for details.

## 👤 Author

Created as a demonstration of LangChain capabilities for educational purposes.

---

**Last Updated**: 2026-06-11
