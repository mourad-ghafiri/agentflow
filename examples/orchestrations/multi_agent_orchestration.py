"""
Multi-agent orchestration example using the AgentFlow framework.
"""
import os
import asyncio
import json
from typing import Dict, List, Any

from dotenv import load_dotenv
from framework.core.app import AgentFlowApp
from framework.core.providers import OpenAIProvider, AnthropicProvider
from framework.tools.base import FunctionTool, PydanticTool
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Define research tools
def search_web(query: str) -> List[Dict[str, str]]:
    """Simulated web search tool.
    
    Args:
        query: The search query.
        
    Returns:
        A list of search results with title and snippet.
    """
    # This is a mock implementation
    return [
        {
            "title": "Example Result 1",
            "snippet": f"This is an example search result for '{query}'. It contains information about the topic."
        },
        {
            "title": "Example Result 2",
            "snippet": f"Another example result for '{query}' with different information and details."
        }
    ]

class ExtractInsightsInput(BaseModel):
    """Input model for extracting insights."""
    text: str = Field(..., description="The text to extract insights from")
    max_insights: int = Field(3, description="Maximum number of insights to extract")

class ExtractInsightsOutput(BaseModel):
    """Output model for extracted insights."""
    insights: List[str] = Field(..., description="The extracted insights")

class InsightExtractionTool(PydanticTool):
    """Tool for extracting insights from text."""
    
    def __init__(self):
        super().__init__(
            name="extract_insights",
            description="Extract key insights from text content",
            input_model=ExtractInsightsInput,
            output_model=ExtractInsightsOutput
        )
    
    async def _execute_with_validated_input(self, validated_input: ExtractInsightsInput) -> ExtractInsightsOutput:
        """Execute insight extraction on the input text."""
        # This is a mock implementation that would normally use an LLM
        insights = [
            f"Insight 1 from the text: {validated_input.text[:20]}...",
            f"Insight 2 from the text: {validated_input.text[20:40]}..."
        ]
        if validated_input.max_insights > 2:
            insights.append(f"Insight 3 from the text: {validated_input.text[40:60]}...")
        
        return ExtractInsightsOutput(insights=insights)

async def main():
    # Check for API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your_openai_api_key_here":
        print("Error: OpenAI API key not found!")
        print("Please set your OPENAI_API_KEY in the .env file.")
        print("Example: OPENAI_API_KEY=sk-...your-key...")
        return
    
    # Create the application
    app = AgentFlowApp(name="Research Assistant System", description="A multi-agent system for research assistance")
    
    # Register providers
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    app.register_provider("openai", OpenAIProvider(api_key=openai_api_key))
    if anthropic_api_key and anthropic_api_key != "your_anthropic_api_key_here":
        app.register_provider("anthropic", AnthropicProvider(api_key=anthropic_api_key))
    
    # Register tools
    app.register_tool(FunctionTool(search_web))
    app.register_tool(InsightExtractionTool())
    
    # Create agents
    
    # 1. Research Agent - Searches for information
    research_agent = app.create_agent(
        agent_type="react",
        name="ResearchAgent",
        description="An agent that performs research by searching the web",
        system_prompt="""You are a research assistant specialized in finding information.
When given a research question or topic, use the search_web tool to find relevant information.
Return the search results along with a brief summary of what you found.""",
        model="gpt-4",
        provider="openai",
        tools=["search_web"]
    )
    
    # 2. Analysis Agent - Analyzes the research results
    analysis_agent = app.create_agent(
        agent_type="react",
        name="AnalysisAgent",
        description="An agent that analyzes research results to extract insights",
        system_prompt="""You are an analysis assistant specialized in extracting insights from research information.
When given research results, analyze them carefully and extract the key insights using the extract_insights tool.
Return the extracted insights along with your reasoning.""",
        model="gpt-4",
        provider="openai",
        tools=["extract_insights"]
    )
    
    # 3. Summary Agent - Creates a final summary
    summary_agent = app.create_agent(
        agent_type="react",
        name="SummaryAgent",
        description="An agent that creates clear, concise summaries",
        system_prompt="""You are a summary specialist who excels at creating clear, concise summaries.
When given a set of insights and analysis, create a final comprehensive summary that ties everything together.
Your summary should be well-structured and easy to understand.""",
        model="gpt-4",
        provider="openai",
        tools=[]
    )
    
    # Create a sequential orchestrator
    orchestrator = await app.create_orchestrator(
        orchestrator_type="sequential",
        name="ResearchWorkflow",
        description="A sequential workflow for research, analysis, and summarization",
        agents=[research_agent.config.id, analysis_agent.config.id, summary_agent.config.id],
        workflow={
            "sequence": [
                research_agent.config.id,
                analysis_agent.config.id,
                summary_agent.config.id
            ]
        }
    )
    
    # Run the orchestrator
    user_input = "I'd like to research the impact of artificial intelligence on healthcare"
    print(f"User request: {user_input}")
    
    response = await app.run_orchestrator(orchestrator.config.id, user_input)
    print(f"\nFinal Summary:\n{response.get('content')}")

if __name__ == "__main__":
    asyncio.run(main()) 