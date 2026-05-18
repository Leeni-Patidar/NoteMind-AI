from crewai import LLM

# Groq API LLM Configuration
groq_llm = LLM(
    model="groq/mixtral-8x7b-32768",
    temperature=0.5
)
