"""
Example of using a FunctionCallingAgent with tools in the AgentFlow framework.
"""
import os
import asyncio
from dotenv import load_dotenv
from framework.core.app import AgentFlowApp
from framework.core.providers import OpenAIProvider
from framework.tools.base import FunctionTool

# Load environment variables
load_dotenv()

# Create weather and location tools (simplified mocks)
def get_weather(location: str, date: str = "today") -> dict:
    """Get the weather forecast for a location."""
    # This is a mock implementation
    weather_data = {
        "paris": {"today": {"condition": "Sunny", "temperature": 22, "humidity": 60}},
        "london": {"today": {"condition": "Rainy", "temperature": 15, "humidity": 80}},
        "new york": {"today": {"condition": "Cloudy", "temperature": 18, "humidity": 70}},
        "tokyo": {"today": {"condition": "Clear", "temperature": 25, "humidity": 55}}
    }
    
    location = location.lower()
    if location not in weather_data:
        return {"error": f"Weather data not available for {location}"}
    
    if date not in weather_data[location]:
        return {"error": f"Weather data not available for {date} in {location}"}
    
    return weather_data[location][date]

def get_location_info(location: str) -> dict:
    """Get information about a location."""
    # This is a mock implementation
    location_data = {
        "paris": {"country": "France", "timezone": "CET", "season": "Summer"},
        "london": {"country": "United Kingdom", "timezone": "GMT", "season": "Summer"},
        "new york": {"country": "United States", "timezone": "EST", "season": "Summer"},
        "tokyo": {"country": "Japan", "timezone": "JST", "season": "Summer"}
    }
    
    location = location.lower()
    if location not in location_data:
        return {"error": f"Location data not available for {location}"}
    
    return location_data[location]

async def main():
    # Check for API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your_openai_api_key_here":
        print("Error: OpenAI API key not found!")
        print("Please set your OPENAI_API_KEY in the .env file.")
        print("Example: OPENAI_API_KEY=sk-...your-key...")
        return
    
    # Create the application
    app = AgentFlowApp(name="Function Calling App", description="An app with a function calling agent")
    
    # Register OpenAI provider
    app.register_provider("openai", OpenAIProvider(api_key=openai_api_key))
    
    # Register tools
    app.register_tool(FunctionTool(get_weather))
    app.register_tool(FunctionTool(get_location_info))
    
    # Create a function calling agent
    agent = app.create_agent(
        agent_type="function_calling",
        name="Weather Assistant",
        description="An agent that can check weather and provide recommendations",
        system_prompt="You are a weather assistant. Use the tools available to check weather and provide recommendations for clothing and activities based on the weather.",
        model="gpt-4",
        provider="openai",
        tools=["get_weather", "get_location_info"]
    )
    
    # Run the agent
    user_input = "What's the weather like in Paris today and what should I wear?"
    print(f"User: {user_input}")
    
    response = await app.run_agent(agent.config.id, user_input)
    print(f"Agent: {response.get('content', 'No content in response')}")

if __name__ == "__main__":
    asyncio.run(main())
