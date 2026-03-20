from crewai import LLM

ollama_llm = LLM(
    model="ollama/phi",
    temperature=0.5
)