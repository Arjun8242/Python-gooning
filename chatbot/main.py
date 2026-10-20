from langchain_core.messages import AIMessage
import os
import sqlite3
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv

load_dotenv()


# Define State 

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL")
)

def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
connection = sqlite3.connect("chatbot.db", check_same_thread=False)
saver = SqliteSaver(connection)
workflow = graph.compile(checkpointer=saver)

if __name__ == "__main__":
    thread_id = input("Thread id (naya ya purana naam): ").strip() or "default"
    config = {"configurable": {"thread_id": thread_id}}

    # Purani history dikhao agar is thread mein pehle se kuch saved hai
    saved = workflow.get_state(config).values.get("messages", [])
    if saved:
        print(f"\n--- {len(saved)} purane messages mile ---")
        for m in saved:
            print(f"{m.type}: {m.content}")
        print("--- yahan se aage ---\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        if not user_input.strip():
            continue

        print("Bot: ", end="", flush=True)

        for chunk, metadata in workflow.stream({"messages": [HumanMessage(content = user_input)]},
        config = config,
        stream_mode = "messages",
        ):

            if isinstance(chunk, AIMessage) and chunk.content:
                print(chunk.content, end="", flush = True)

        print()
        print()