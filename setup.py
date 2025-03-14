from setuptools import setup, find_packages

setup(
    name="agentflow",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "langchain>=0.1.0",
        "openai>=1.0.0",
        "anthropic>=0.8.0",
        "instructor>=0.4.0",
        "httpx>=0.25.0",
        "python-dotenv>=1.0.0",
        "jsonschema>=4.0.0",
        "typing-extensions>=4.5.0",
        "rich>=13.0.0",
    ],
    author="Mourad GHAFIRI",
    description="AgentFlow framework for building AI agents",
    keywords="ai, agents, llm, openai, anthropic",
    python_requires=">=3.8",
) 