from crewai import LLM

ollama_llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434",
    temperature=0.5,
    max_tokens=800   
)