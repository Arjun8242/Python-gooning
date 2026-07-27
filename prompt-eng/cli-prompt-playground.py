import os
import sys
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from groq import Groq

# Load environment variables
load_dotenv()

client = Groq()

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')#Prevents Windows terminal crashes when the model returns special characters (bullet points, smart quotes, etc.).
        
    print("=== CLI Prompt Playground ===\n")
    
    role = input("Role: ").strip()
    task = input("Task: ").strip()
    context = input("Context: ").strip()
    constraints = input("Constraints: ").strip()
    output_format = input("Output Format: ").strip()

    prompt = f"""You are {role}.

Task:
{task}

Context:
\"\"\"
{context}
\"\"\"

Constraints:
{constraints}

Output Format:
{output_format}"""

    print("\n--- Generated Prompt ---")
    print(prompt)

    print("\n--- Response ---")
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
