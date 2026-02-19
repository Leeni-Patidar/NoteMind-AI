from crewai import Agent
from llm.ollama_llm import ollama_llm

rag_agent = Agent(
    role="RAG Agent",
    goal="Retrieve relevant information from vector database",
    backstory="Expert in retrieving educational content",
    llm=ollama_llm,  
    verbose=True
)
