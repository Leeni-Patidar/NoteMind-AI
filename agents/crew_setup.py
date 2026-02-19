from crewai import Crew, Task
from agents.researcher_agent import research_agent
from agents.rag_agent import rag_agent
from agents.writer_agent import writer_agent
import ollama
from config import LLM_MODEL


def run_notes(topic, mode):

    prompt = f"""
    Generate {mode} notes on {topic}

    structured and clear
    """

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


def run_questions(topic, qtype, number):

    prompt = f"""
    Generate {number} {qtype} questions with answers on {topic}
    """

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
