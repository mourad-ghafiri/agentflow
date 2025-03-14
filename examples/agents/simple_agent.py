"""
Simple agent example using the AgentFlow framework.
This demonstrates the most basic usage of the framework with a simple conversational agent.
"""
import os
import asyncio
from dotenv import load_dotenv
from framework.core.app import AgentFlowApp
from framework.core.providers import OpenAIProvider

# Load environment variables
load_dotenv()

async def main():
    # Check for API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OpenAI API key not found!")
        print("Please set your OPENAI_API_KEY in the .env file.")
        return
    
    # Create the application
    app = AgentFlowApp(
        name="Simple Agent App", 
        description="A minimal example of using the AgentFlow framework"
    )
    
    # Register OpenAI provider
    app.register_provider("openai", OpenAIProvider(api_key=openai_api_key))
    
    # Create a simple agent
    agent = app.create_agent(
        agent_type="conversational",  # Using the simplest agent type
        name="SimpleAgent",
        description="A simple conversational agent",
        system_prompt="You are a helpful assistant. Keep your responses brief and to the point.",
        model="gpt-3.5-turbo",  # Using a less expensive model for this simple example
        provider="openai"
    )
    
    # Run the agent with a simple query
    user_input = "Hello! Can you tell me what the AgentFlow framework is?"
    print(f"User: {user_input}")
    
    response = await app.run_agent(agent.config.id, user_input)
    print(f"Agent: {response.get('content', 'No response generated')}")

if __name__ == "__main__":
    asyncio.run(main())