from crewai import Agent
from llm.ollama_llm import ollama_llm

writer_agent = Agent(
    role="Writer Agent",
    goal="Write structured notes from research",
    backstory="Expert educational content writer",
    llm=ollama_llm,
    verbose=True
)
