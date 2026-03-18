from crewai import Crew, Task
from agents.researcher_agent import research_agent
from agents.rag_agent import rag_agent
from agents.writer_agent import writer_agent
import ollama
from config import LLM_MODEL


# ================= NOTES =================
def run_notes(topic, mode):
    try:
        prompt = f"""
        Create {mode} notes on: {topic}

        Keep it:
        - Clear
        - Structured
        - Concise
        """

        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.5,
                "num_predict": 700   # 🔥 LIMIT TOKENS = SPEED BOOST
            }
        )

        return response["message"]["content"]

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ================= QUESTIONS =================
def run_questions(topic, qtype, number):
    try:
        prompt = f"""
        Generate {number} {qtype} questions with answers on: {topic}

        Keep answers short and clear.
        """

        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.5,
                "num_predict": 700   # 🔥 SPEED CONTROL
            }
        )

        return response["message"]["content"]

    except Exception as e:
        return f"❌ Error: {str(e)}"