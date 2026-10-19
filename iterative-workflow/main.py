import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

writer_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.7)
judge_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
optimizer_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.7)

APPROVED_SCORE = 8


class TweetState(TypedDict):
    topic: str
    tweet: str
    score: int
    feedback: str
    iteration: int
    max_iteration: int


class TweetEvaluation(TypedDict):
    score: int
    feedback: str


structured_judge = judge_llm.with_structured_output(TweetEvaluation, method="json_schema")


WRITER_SYSTEM = """
You are a witty, sarcastic tech Twitter writer. You write ONE tweet per request.

Style:
- Dry, observational humor. Sarcasm should land on the situation, never attack a person or group.
- The first line must work as a hook: a bold claim, a relatable pain, or an unexpected twist.
- Be specific. A concrete detail beats a generic joke.
- Plain language. No corporate tone, no "Did you know", no "Here's a thread".
- At most one emoji, and only if it adds to the joke. Max 1 hashtag.

Hard rules:
- Maximum 280 characters.
- Return ONLY the tweet text. No quotes around it, no preamble, no explanation.
"""

JUDGE_SYSTEM = """
You are a strict, no-nonsense judge of tech humor. Most tweets are mediocre (4-6).
Give 8+ only if the tweet is genuinely good.
Feedback must be specific and actionable, e.g. "the hook is generic, open with the pain point itself".
Never just say "make it funnier".
"""

OPTIMIZER_SYSTEM = """
You punch up tweets for tech Twitter. Keep what works, fix what the editor flagged.
Maximum 280 characters. Return ONLY the improved tweet text, no quotes, no explanation.
"""


def writer_node(state: TweetState):
    messages = [
        SystemMessage(content=WRITER_SYSTEM),
        HumanMessage(content=f'Write a tweet about: "{state["topic"]}"'),
    ]
    response = writer_llm.invoke(messages)
    return {"tweet": response.content.strip()}


def judge_node(state: TweetState):
    messages = [
        SystemMessage(content=JUDGE_SYSTEM),
        HumanMessage(content=f"""
Topic: {state['topic']}

Tweet:
"{state['tweet']}"

Score this tweet from 1 to 10 (1 = garbage, 10 = comedy gold) and give feedback.
"""),
    ]
    response = structured_judge.invoke(messages)
    return {"score": response["score"], "feedback": response["feedback"]}


def optimizer_node(state: TweetState):
    messages = [
        SystemMessage(content=OPTIMIZER_SYSTEM),
        HumanMessage(content=f"""
Topic: "{state['topic']}"

Current tweet:
"{state['tweet']}"

Editor feedback:
"{state['feedback']}"

Rewrite the tweet fixing this feedback.
"""),
    ]
    response = optimizer_llm.invoke(messages)
    return {"tweet": response.content.strip(), "iteration": state["iteration"] + 1}


def router(state: TweetState):
    if state["score"] >= APPROVED_SCORE or state["iteration"] >= state["max_iteration"]:
        return "approved"
    return "need_improvement"


builder = StateGraph(TweetState)

builder.add_node("writer", writer_node)
builder.add_node("judge", judge_node)
builder.add_node("optimizer", optimizer_node)

builder.add_edge(START, "writer")
builder.add_edge("writer", "judge")
builder.add_edge("optimizer", "judge")
builder.add_conditional_edges("judge", router, {"approved": END, "need_improvement": "optimizer"})

graph = builder.compile()

result = graph.invoke({"topic": "AI is the end of humanity", "iteration": 0, "max_iteration": 3})

print(result)