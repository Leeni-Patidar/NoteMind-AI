from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_handoff_tool, create_swarm
import os

# -------------------------
# Gemini API Key
# -------------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyDsN-2KwLKJ3pipgoLBRQ-RvJ48j6UDUa4"

# -------------------------
# Initialize Gemini model
# -------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# -------------------------
# Tools
# -------------------------
def question_answering(question: str):
    """Answers general knowledge questions."""
    return llm.invoke(question).content

def science_tool(question: str):
    """Answers science-related questions."""
    return llm.invoke(question).content

def extract_language_and_text(request: str):
    request = request.lower()
    to_patterns = [" to ", " in ", " into "]
    target_language = None
    text = request

    for pattern in to_patterns:
        if pattern in request:
            parts = request.split(pattern)
            if len(parts) == 2:
                text = parts[0]
                target_language = parts[1].strip()
                break

    text = text.replace("translate", "").replace("say", "").strip()
    return text.strip(), target_language

def translate_text(request: str):
    """Translates text to a specified language."""
    if any(x in request.lower() for x in [
        "help with", "can you", "need translation", "translate something"
    ]):
        return (
            "I can help you translate. Use:\n"
            "'translate [text] to [language]' or '[text] in [language]'"
        )

    text, target_language = extract_language_and_text(request)

    if not target_language:
        return (
            f"I need the target language to translate: '{text}'. "
            "Please specify the language in your next message."
        )

    prompt = f"Translate the following text to {target_language}:\n{text}"
    return llm.invoke(prompt).content

# -------------------------
# Agents
# -------------------------
question_answering_agent = create_react_agent(
    model=llm,
    tools=[
        question_answering,
        create_handoff_tool(agent_name="science_agent"),
        create_handoff_tool(agent_name="translator_agent"),
    ],
    name="question_answering_agent",
    prompt=(
        "You are a general question answering agent. "
        "Route science questions to science_agent and "
        "translation requests to translator_agent. "
        "Only answer general knowledge questions."
    ),
)

science_agent = create_react_agent(
    model=llm,
    tools=[
        science_tool,
        create_handoff_tool(agent_name="question_answering_agent"),
        create_handoff_tool(agent_name="translator_agent"),
    ],
    name="science_agent",
    prompt=(
        "You are a science expert. Answer science questions only. "
        "Route non-science to question_answering_agent and "
        "translations to translator_agent."
    ),
)

translator_agent = create_react_agent(
    model=llm,
    tools=[
        translate_text,
        create_handoff_tool(agent_name="question_answering_agent"),
        create_handoff_tool(agent_name="science_agent"),
    ],
    name="translator_agent",
    prompt=(
        "You are a translation agent. Your main goal is to accurately translate text. "
        "When the user asks for a translation, your ONLY task is to call the "
        "'translate_text' tool. "
        "For the 'request' argument, pass the ENTIRE user message unmodified. "
        "If the tool requests a target language, return that message directly. "
        "Route science questions to science_agent and general questions to "
        "question_answering_agent."
    ),
)

# -------------------------
# Swarm & Memory
# -------------------------
checkpoint = InMemorySaver()

workflow = create_swarm(
    agents=[
        question_answering_agent,
        science_agent,
        translator_agent
    ],
    default_active_agent="question_answering_agent",
)

app = workflow.compile(checkpointer=checkpoint)

# -------------------------
# Save graph
# -------------------------
image = app.get_graph().draw_mermaid_png()
with open("swarm.png", "wb") as f:
    f.write(image)

# -------------------------
# Run
# -------------------------
config = {"configurable": {"thread_id": "1"}}

while True:
    user_input = input("\nEnter your request (or 'exit'): ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    result = app.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
    )

    for m in result["messages"]:
        print(m.pretty_print())
