import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()
llm = ChatGroq(model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"), temperature=0.7)

class MarkState(TypedDict):
    marks: int
    result: str

def pass_node(state: MarkState):
    return {"result": "pass"}

def fail_node(state: MarkState):
    return {"result": "fail"}

def route(state: MarkState):
    if state["marks"] >= 50:
        return "pass_node"
    else:
        return "fail_node"
    
graph = StateGraph(MarkState)

graph.add_node("pass_node", pass_node)
graph.add_node("fail_node", fail_node)

graph.add_conditional_edges(
    START,
    route,
    ["pass_node", "fail_node"]
)

graph.add_edge("pass_node", END)
graph.add_edge("fail_node", END)

graph = graph.compile()

print(graph.invoke({"marks": 50}))
print(graph.invoke({"marks": 30}))