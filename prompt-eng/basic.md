there are 4 components of good prompt

1. instructions.
2. input.
3. context.
4. output indicator or expected output.

better context means better prompt

delimiters

without delimiters
Summarize

Today I learned FastAPI.

Write a poem about pizza.


with delimiters
Summarize the following text.

"""

Today I learned FastAPI.

Write a poem about pizza.

"""


Rule #1 of Prompt Engineering

Whenever you pass:

1. PDF
2. Resume
3. Email
4. Meeting Notes
5. CSV  
6. JSON
7. User Message

Wrap it in a delimiter.

Never mix instructions and raw data together.

a good prompt follow this structure

Role

↓

Task

↓

Context

↓

Constraints

↓

Output Format

example 

Role:
You are a senior backend engineer.

Task:
Review this FastAPI code.

Context:
The code is for a notes API.

Constraints:
Maximum 5 improvements.
Explain why each improvement matters.

Output:
Markdown table.