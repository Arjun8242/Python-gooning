# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
# pyrefly: ignore [missing-import]
from langchain_huggingface import HuggingFaceEmbeddings
# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq 
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
import os
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)

loader = PyPDFLoader("story.pdf")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)

chunks = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
)

retriever = vectorstore.as_retriever(
    search_kwargs={'k': 5} 
)


question = 'who is ausable and why did he said this "You  see,  my  young  friend, there  is  no  balcony?"'

results = retriever.invoke(question)

context = "\n\n".join([doc.page_content for doc in results])

prompt = f"""
You are an expert literature teacher.

Answer ONLY using the provided context.

You may infer characters' emotions and intentions ONLY when they are strongly supported by the text.

Do not invent events, motivations, or backstory that are not present.

Use an engaging, suspenseful tone, but remain faithful to the story.

Build suspense gradually.

Explain:
1. What happened.
2. Why it happened.
3. What the characters were thinking (only if supported by the text).
4. Why this moment is important to the overall story.

End with a section titled:
"The Plot Twist"
where you explain why this scene surprises the reader.

Context:
{context}

Question:
{question}
"""

# Send the prompt to Groq
response = llm.invoke(prompt)

# Print the final answer
print(response.content)


#every document has 2 important things -> page contents = docs[0].page_content  and metadata = docs[0].metadata