"""
DAG-based orchestration example using the AgentFlow framework.
"""
import os
import asyncio
import json
from typing import Dict, List, Any

from dotenv import load_dotenv
from framework.core.app import AgentFlowApp
from framework.core.providers import OpenAIProvider
from framework.tools.base import FunctionTool
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Define some sample tools
def fetch_user_preferences(user_id: str) -> Dict[str, Any]:
    """Fetches user preferences from a simulated database.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        A dictionary of user preferences.
    """
    # This is a mock implementation
    return {
        "interests": ["AI", "machine learning", "data science"],
        "content_type_preference": "article",
        "technical_level": "intermediate"
    }

def fetch_latest_content(category: str, count: int = 3) -> List[Dict[str, str]]:
    """Fetches the latest content in a category.
    
    Args:
        category: The content category.
        count: Number of items to fetch.
        
    Returns:
        A list of content items.
    """
    # This is a mock implementation
    return [
        {
            "title": f"{category} News Item 1",
            "summary": f"This is a summary of the latest news in {category}.",
            "technical_level": "beginner"
        },
        {
            "title": f"{category} Tutorial 1",
            "summary": f"A step-by-step tutorial about {category} concepts.",
            "technical_level": "intermediate"
        },
        {
            "title": f"Advanced {category} Concepts",
            "summary": f"Deep dive into advanced {category} topics.",
            "technical_level": "advanced"
        }
    ][:count]

def generate_personalized_summary(content: List[Dict[str, Any]], preferences: Dict[str, Any]) -> str:
    """Generate a personalized summary based on content and user preferences.
    
    This is a mock function that would normally be implemented as an agent itself.
    
    Args:
        content: Content items to summarize.
        preferences: User preferences.
        
    Returns:
        A personalized summary.
    """
    # This is a mock implementation
    filtered_content = [
        item for item in content 
        if item.get("technical_level") == preferences.get("technical_level", "intermediate")
    ]
    return f"Here's a personalized summary based on your {preferences.get('technical_level', 'intermediate')} level in {', '.join(preferences.get('interests', []))}:\n\n" + "\n".join(
        [f"- {item['title']}: {item['summary']}" for item in filtered_content]
    )

async def main():
    # Check for API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your_openai_api_key_here":
        print("Error: OpenAI API key not found!")
        print("Please set your OPENAI_API_KEY in the .env file.")
        print("Example: OPENAI_API_KEY=sk-...your-key...")
        return
        
    # Create the application
    app = AgentFlowApp(name="Content Recommendation System", description="A multi-agent system for content recommendations")
    
    # Register providers
    app.register_provider("openai", OpenAIProvider(api_key=openai_api_key))
    
    # Register tools
    app.register_tool(FunctionTool(fetch_user_preferences))
    app.register_tool(FunctionTool(fetch_latest_content))
    app.register_tool(FunctionTool(generate_personalized_summary))
    
    # Create agents
    
    # 1. User Profile Agent - Gets user preferences
    profile_agent = app.create_agent(
        agent_type="react",
        name="ProfileAgent",
        description="An agent that fetches and interprets user profile information",
        system_prompt="""You are a user profile specialist. When you receive a user ID,
use the fetch_user_preferences tool to get the user's preferences.
Return the preferences along with a brief interpretation of what these preferences mean.""",
        model="gpt-3.5-turbo",
        provider="openai",
        tools=["fetch_user_preferences"]
    )
    
    # 2. Content Discovery Agent - Finds content for each interest
    discovery_agent = app.create_agent(
        agent_type="react",
        name="DiscoveryAgent",
        description="An agent that discovers relevant content based on user interests",
        system_prompt="""You are a content discovery specialist. When you receive user interests,
fetch the latest content for each interest using the fetch_latest_content tool.
Combine the results and return them.""",
        model="gpt-3.5-turbo",
        provider="openai",
        tools=["fetch_latest_content"]
    )
    
    # 3. Personalization Agent - Personalizes content based on user preferences
    personalization_agent = app.create_agent(
        agent_type="react",
        name="PersonalizationAgent",
        description="An agent that personalizes content based on user preferences",
        system_prompt="""You are a content personalization specialist. When you receive content and user preferences,
use the generate_personalized_summary tool to create a personalized summary.
Return the personalized summary.""",
        model="gpt-3.5-turbo",
        provider="openai",
        tools=["generate_personalized_summary"]
    )
    
    # 4. Presentation Agent - Creates a final presentation
    presentation_agent = app.create_agent(
        agent_type="react",
        name="PresentationAgent",
        description="An agent that creates a final presentation",
        system_prompt="""You are a presentation specialist. When you receive personalized content,
create a final presentation with a friendly introduction, the content, and a closing statement.
Make it conversational and engaging.""",
        model="gpt-4",
        provider="openai",
        tools=[]
    )
    
    # Create a DAG orchestrator
    orchestrator = await app.create_orchestrator(
        orchestrator_type="dag",
        name="RecommendationWorkflow",
        description="A DAG workflow for personalized content recommendations",
        agents=[
            profile_agent.config.id, 
            discovery_agent.config.id, 
            personalization_agent.config.id,
            presentation_agent.config.id
        ],
        workflow={
            "entry_point": profile_agent.config.id,
            "final_node": presentation_agent.config.id,
            "dag": {
                profile_agent.config.id: {
                    "dependencies": [],
                    "description": "Fetch user profile information"
                },
                discovery_agent.config.id: {
                    "dependencies": [profile_agent.config.id],
                    "description": "Discover content based on user interests",
                    "input_mapping": {
                        "interests": f"{profile_agent.config.id}"
                    }
                },
                personalization_agent.config.id: {
                    "dependencies": [profile_agent.config.id, discovery_agent.config.id],
                    "description": "Personalize content based on user preferences and discovered content",
                    "input_mapping": {
                        "content": f"{discovery_agent.config.id}",
                        "preferences": f"{profile_agent.config.id}"
                    }
                },
                presentation_agent.config.id: {
                    "dependencies": [personalization_agent.config.id],
                    "description": "Create final presentation"
                }
            }
        }
    )
    
    # Run the orchestrator
    user_input = "user_12345"  # This would normally be a user ID
    print(f"Processing recommendations for user: {user_input}")
    
    response = await app.run_orchestrator(orchestrator.config.id, user_input)
    print(f"\nFinal Recommendation:\n{response.get('content')}")

if __name__ == "__main__":
    asyncio.run(main()) 