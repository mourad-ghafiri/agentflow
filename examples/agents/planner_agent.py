"""
Example of using a PlannerAgent in the AgentFlow framework.
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
    app = AgentFlowApp(name="Planner App", description="An app with a planner agent")
    
    # Register OpenAI provider
    app.register_provider("openai", OpenAIProvider(api_key=openai_api_key))
    
    # Create a planner agent
    agent = app.create_agent(
        agent_type="planner",
        name="Trip Planner",
        description="An agent that creates travel plans",
        system_prompt="""You are a travel planner. Create detailed travel plans with steps, activities, and recommendations.
Format your response as a JSON object with the following structure:
{
  "description": "Brief overview of the trip plan",
  "steps": [
    {
      "description": "Detailed description of each step or day of the trip"
    }
  ]
}""",
        model="gpt-4",
        provider="openai"
    )
    
    # Run the agent
    user_input = "Plan a 3-day trip to Tokyo for a family with two children."
    print(f"User: {user_input}")
    
    plan = await app.run_agent(agent.config.id, user_input)
    
    # Handle the case where the response might not be properly formatted
    if isinstance(plan, dict) and 'description' in plan and 'steps' in plan:
        print(f"Plan description: {plan['description']}")
        print("Steps:")
        for i, step in enumerate(plan['steps'], 1):
            if isinstance(step, dict) and 'description' in step:
                print(f"{i}. {step['description']}")
            else:
                print(f"{i}. {step}")
    else:
        print("Received response was not in the expected format:")
        print(plan)

if __name__ == "__main__":
    asyncio.run(main())
