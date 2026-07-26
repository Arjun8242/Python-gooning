# OpenAI SDK Phase 2 --- Deep Interview Notes

> Goal: Understand these topics at the level expected from an AI
> Engineer interview, not just how to call an SDK.

------------------------------------------------------------------------

# 1. Authentication

## Interview Question

**Q: What is authentication in the OpenAI SDK and why is it necessary?**

Authentication proves your application's identity to OpenAI. Every API
request must include valid credentials so OpenAI knows: - Who made the
request - Which project is being billed - Which models/features can be
accessed - Rate limits that apply

Without authentication, the API returns **401 Unauthorized**.

## API Keys

API keys are secret credentials.

``` python
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY")
```

Never hardcode keys in source code.

Instead:

``` text
OPENAI_API_KEY=sk-xxxxxxxx
```

``` python
from openai import OpenAI

client = OpenAI()
```

The SDK automatically reads `OPENAI_API_KEY`.

## Why Environment Variables?

Interview answer: - Prevent accidental GitHub leaks - Different keys for
development/production - Easier deployment - Better security practices

## Follow-up Questions

### Why not store API keys in Git?

Attackers continuously scan public repositories for leaked keys.

### What happens if the key expires?

Every request fails until a valid key is supplied.

------------------------------------------------------------------------

# 2. Basic Text Generation

Everything starts with:

User Input → Prompt → Model → Response

``` python
response = client.responses.create(
    model="gpt-5",
    input="Explain JWT."
)
```

## What actually happens?

1.  SDK creates HTTPS request.
2.  Request reaches OpenAI.
3.  Model tokenizes prompt.
4.  Transformer predicts next tokens.
5.  Tokens become text.
6.  SDK returns response.

## Interview Question

**Difference between prompt and response?**

Prompt: Information given to the model.

Response: Model-generated output.

## Good Prompt Characteristics

-   Clear
-   Specific
-   Context-rich
-   Constrained

Bad:

> Explain Python.

Better:

> Explain Python decorators with backend examples in under 200 words.

------------------------------------------------------------------------

# 3. System Prompt

## Interview Question

What is a system prompt?

A high-priority instruction controlling the assistant's behavior.

Hierarchy:

1.  System Prompt
2.  Developer Instructions
3.  User Prompt

Example:

System:

> You are a senior backend engineer.

User:

> Explain REST APIs.

Response will stay technical.

## Use Cases

-   Customer Support
-   Medical Assistant
-   Coding Tutor
-   Financial Advisor
-   Legal Assistant

## Common Mistake

Beginners place permanent instructions inside every user prompt instead
of the system prompt.

------------------------------------------------------------------------

# 4. Structured Outputs

This is one of the most important production features.

Instead of:

``` text
The candidate scored 90.
```

Return:

``` json
{
  "score":90,
  "hire":true
}
```

## Why?

Backend services consume structured data much more reliably than
free-form text.

Example:

``` python
if result["score"] > 80:
    hire()
```

No fragile string parsing.

## Real Applications

-   Resume screening
-   Invoice extraction
-   Medical reports
-   Workout plans
-   Expense categorization
-   Recommendation engines

## Interview Question

Why not parse plain text?

Because LLM wording varies between calls. Structured outputs reduce
ambiguity and simplify automation.

------------------------------------------------------------------------

# 5. Streaming

Normally:

Request → Wait → Full response

Streaming:

Request → Token → Token → Token → Finished

Example:

``` python
stream = client.responses.create(
    model="gpt-5",
    input="Explain JWT",
    stream=True,
)

for event in stream:
    pass
```

## Benefits

-   Lower perceived latency
-   Better UX
-   Early rendering
-   Cancellation support

## Interview Question

Does streaming make the model faster?

No.

Generation speed is similar.

Streaming simply sends partial output immediately.

------------------------------------------------------------------------

# 6. Images

Models can generate images from natural language.

Applications:

-   Marketing
-   Logo generation
-   Character design
-   Product mockups
-   Game assets

Backend flow:

Prompt → Image Model → Image URL/File

Interview note: Text and image generation are separate capabilities
optimized for different modalities.

------------------------------------------------------------------------

# 7. File Input

Instead of typing everything manually, upload files.

Examples:

-   PDFs
-   Images
-   Word documents
-   Text files

Applications:

-   Resume parser
-   Contract analyzer
-   Invoice extraction
-   Research assistant

## Relation to RAG

File upload is NOT RAG.

RAG additionally performs:

Documents → Chunking → Embeddings → Vector Database → Retrieval → LLM

The retrieved chunks become context for the model.

------------------------------------------------------------------------

# Frequently Asked Interview Questions

### Why use environment variables?

Security and deployment flexibility.

### Why are system prompts important?

They define consistent behavior across conversations.

### Why prefer structured outputs?

Reliable backend integration and automation.

### Does streaming reduce inference time?

No. It improves perceived responsiveness.

### Is uploading a PDF the same as RAG?

No. RAG requires retrieval from indexed knowledge.

------------------------------------------------------------------------

# Production Learning Order

1.  Authentication
2.  Basic generation
3.  Prompt engineering
4.  System prompts
5.  Structured outputs
6.  Streaming
7.  File inputs
8.  Function/tool calling
9.  MCP
10. Agents
11. Multi-agent systems

Master these topics before moving to tool calling and agents because
nearly every production AI application builds on them.
