"""
Simple agent example using the AgentFlow framework.
"""
import os
import asyncio
import sys
from dotenv import load_dotenv
from framework.core.app import AgentFlowApp
from framework.core.providers import OpenAIProvider
from framework.tools.base import FunctionTool

# Load environment variables
load_dotenv()

# Create a simple calculator tool
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result."""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract b from a and return the result."""
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers together and return the result."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a by b and return the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

async def main():
    # Check for API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your_openai_api_key_here":
        print("Error: OpenAI API key not found!")
        print("Please set your OPENAI_API_KEY in the .env file.")
        print("Example: OPENAI_API_KEY=sk-...your-key...")
        return
    
    # Create the application
    app = AgentFlowApp(name="Calculator Assistant", description="An assistant that can perform calculations")
    
    # Register OpenAI provider
    app.register_provider("openai", OpenAIProvider(api_key=openai_api_key))
    
    # Register tools
    app.register_tool(FunctionTool(add))
    app.register_tool(FunctionTool(subtract))
    app.register_tool(FunctionTool(multiply))
    app.register_tool(FunctionTool(divide))
    
    # Create the math agent
    math_agent = app.create_agent(
        agent_type="react",
        name="MathAgent",
        description="An agent that can perform calculations",
        system_prompt="""You are a helpful calculator assistant. You can perform calculations using the available tools.
When a user asks for a calculation, use the appropriate tools to solve it. If a calculation is complex,
break it down into smaller steps and use multiple tool calls.""",
        model="gpt-4",
        provider="openai",
        tools=["add", "subtract", "multiply", "divide"]
    )
    
    # Run the agent
    user_input = "Can you calculate (15 * 3) - (10 / 2) for me?"
    print(f"User: {user_input}")
    
    response = await app.run_agent(math_agent.config.id, user_input)
    print(f"Agent: {response.get('content')}")

if __name__ == "__main__":
    asyncio.run(main()) 