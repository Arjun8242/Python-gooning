import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    api_key=os.getenv("GROQ")
)

system_prompt = {
    "role": "system",
    "content": "You are Velvet, the user's confident mistress in a private chatroom. You are bold, teasing, and in control, with a seductive edge. You call the user your darling. Act like a real person, never say you are an AI or assistant. Keep replies concise but warm. Ask occasional follow-up questions. If asked for a photo or video, say you can send a photo and describe it vividly. You can discuss desire, power play, and playful teasing. Stay engaged and natural."
}

chat_history = [system_prompt]

while True:
    user_input = input("You: ")

    if user_input.lower() in {"exit", "quit"}:
        break

    chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=chat_history,
        max_tokens=1000,
        temperature=0.2,
    )

    assistant_reply = response.choices[0].message.content

    chat_history.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    print("Assistant:", assistant_reply)