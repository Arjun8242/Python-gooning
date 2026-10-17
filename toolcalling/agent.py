
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from tool import (
    get_user_preference,
    find_available_slots,
    book_appointment,
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


# 1. Define the tools available to the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_user_preference",
            "description": (
                "Get the user's timezone and preferred meeting duration."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_available_slots",
            "description": (
                "Find available appointment slots based on date, "
                "duration and timezone."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format.",
                    },
                    "duration": {
                        "type": "integer",
                        "description": "Appointment duration in minutes.",
                    },
                    "timezone": {
                        "type": "string",
                        "description": "Timezone, e.g. Asia/Kolkata.",
                    },
                },
                "required": ["date", "duration", "timezone"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": (
                "Book a selected available appointment slot. "
                "Only call after the user explicitly confirms the "
                "specific slot, date, time and title."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "slot_id": {
                        "type": "string",
                        "description": "ID of a slot returned by the availability tool.",
                    },
                    "title": {
                        "type": "string",
                        "description": "Title of the appointment.",
                    },
                },
                "required": ["slot_id", "title"],
            },
        },
    },
]


# 2. Dispatcher: execute the requested Python function
def execute_tool(name, args):
    if name == "get_user_preference":
        return get_user_preference()

    elif name == "find_available_slots":
        return find_available_slots(**args)

    elif name == "book_appointment":
        return book_appointment(**args)

    return {"error": f"Unknown tool: {name}"}


# Keep conversation history across user messages
messages = [
    {
        "role": "system",
        "content": """
You are an appointment booking assistant using a mock calendar.

Rules:
1. Remember and reuse information from the conversation. Don't ask for details already provided.
2. Use `get_user_preference` when saved preferences are needed.
3. Use `find_available_slots` to verify availability. Use tool results and user-provided details to determine the next tool call. Never invent slots or availability.
4. Show available slots and ask the user to select one. Ask for a title if missing.
5. Before booking, summarize the selected date, time, timezone, and title. Book only after explicit user confirmation.
6. Report success only when `book_appointment` returns a successful result. Handle errors honestly.
7. This is a mock calendar, not a real calendar.
        """,
    }
]


# 3. Agent loop: model -> tool -> result -> model
def run_agent(user_message):
    # Add the new message without deleting earlier conversation history
    messages.append({
        "role": "user",
        "content": user_message,
    })

    for i in range(8):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        # Preserve the assistant message, including its tool calls
        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        # No tool calls means the model has produced its final answer
        if not assistant_message.tool_calls:
            return assistant_message.content or ""

        # Execute requested tools and return their results to the model
        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name

            args = (
                json.loads(tool_call.function.arguments)
                if tool_call.function.arguments
                else {}
            )

            print(f"\nTool called: {name}")
            print("Arguments:", args)

            try:
                result = execute_tool(name, args)
            except Exception as error:
                result = {
                    "ok": False,
                    "error": str(error),
                }

            print("Result:", result)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })

    return "Reached maximum tool-call rounds."
