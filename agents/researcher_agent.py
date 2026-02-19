from crewai import Agent
from tools.search_tool import DuckDuckGoSearchTool
from llm.ollama_llm import ollama_llm

search_tool = DuckDuckGoSearchTool()

research_agent = Agent(
    role="Research Agent",
    goal="Search internet and collect educational content",
    backstory="Expert researcher who finds accurate study material",
    tools=[search_tool],
    llm=ollama_llm,
    verbose=True
)
