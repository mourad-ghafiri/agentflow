"""
Example of using a ConversationalAgent in the AgentFlow framework.
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
    if not openai_api_key or openai_api_key == "your_openai_api_key_here":
        print("Error: OpenAI API key not found!")
        print("Please set your OPENAI_API_KEY in the .env file.")
        print("Example: OPENAI_API_KEY=sk-...your-key...")
        return
    
    # Create the application
    app = AgentFlowApp(name="Conversation App", description="A simple conversational agent app")
    
    # Register OpenAI provider
    app.register_provider("openai", OpenAIProvider(api_key=openai_api_key))
    
    # Create a conversational agent
    agent = app.create_agent(
        agent_type="conversational",
        name="Chat Assistant",
        description="A helpful chat assistant",
        system_prompt="You are a friendly and helpful assistant. Respond concisely and accurately.",
        model="gpt-4",
        provider="openai"
    )
    
    # Run the agent
    user_input = "What is machine learning?"
    print(f"User: {user_input}")
    
    response = await app.run_agent(agent.config.id, user_input)
    print(f"Agent: {response.get('content', 'No content in response')}")

if __name__ == "__main__":
    asyncio.run(main())