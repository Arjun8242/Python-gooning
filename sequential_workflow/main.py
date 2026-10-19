import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()
llm = ChatGroq(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), temperature=0.7)

class BlogState(TypedDict):
    topic: str
    outline: str
    draft: str
    final: str

def make_outline(state: BlogState):
    msg = llm.invoke(f"Create a clear blog outline (headings and bullet points) on: {state['topic']}")

    return {"outline": msg.content}

def write_blog(state: BlogState):
    msg = llm.invoke(
        f"Write a blog post following this outline. Topic: {state['topic']}\n\nOutline:\n{state['outline']}"
    )

    return {"draft": msg.content}


def fix_grammar(state: BlogState):
    msg = llm.invoke(
        "Fix grammar and spelling only. Do not change the meaning or structure. "
        f"Return only the corrected text.\n\n{state['draft']}"
    )

    return {"final": msg.content}


graph = StateGraph(BlogState)

graph.add_node("make_outline", make_outline)
graph.add_node("write_blog", write_blog)
graph.add_node("fix_grammar", fix_grammar)

graph.add_edge(START, "make_outline")
graph.add_edge("make_outline", "write_blog")
graph.add_edge("write_blog", "fix_grammar")
graph.add_edge("fix_grammar", END)

graph = graph.compile()

if __name__ == "__main__":
    out = graph.invoke({"topic": "Why backend developers should learn Redis"})
    print("OUTLINE:\n", out["outline"])
    print("\nFINAL:\n", out["final"])