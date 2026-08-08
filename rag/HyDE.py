from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))

loader = PyPDFLoader("story.pdf")
docs = loader.load()
chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={'k': 5})

question = "How does the story demonstrate that intelligence can be more powerful than physical strength?"

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """...same as before..."""),
    ("human", "Context:\n{context}\n\nQuestion:\n{input}")
])
document_chain = create_stuff_documents_chain(llm, prompt_template)

# --- Plain retrieval baseline ---
retrieval_chain = create_retrieval_chain(retriever, document_chain)
plain_response = retrieval_chain.invoke({"input": question})
print("PLAIN:\n", plain_response["answer"])

# --- HyDE retrieval ---
hyde_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are helping with document retrieval.
Given a question about a story, write a short, plausible passage (3-5 sentences)
that could appear in the source text and would answer this question.
Write it in narrative style, as if it were an excerpt from the story itself.
Do not hedge, do not say you don't know — just write the passage."""),
    ("human", "{question}")
])
hyde_chain = hyde_prompt | llm

def hyde_retrieve(question, k=5):
    hypothetical_doc = hyde_chain.invoke({"question": question}).content

    print("\n===== HYPOTHETICAL DOCUMENT =====")
    print(hypothetical_doc)

    hyde_vector = embeddings.embed_query(hypothetical_doc)
    return vectorstore.similarity_search_by_vector(hyde_vector, k=k)

hyde_docs = hyde_retrieve(question)

print("\n===== HYDE RETRIEVED DOCUMENTS =====")

for i, doc in enumerate(hyde_docs):
    print(f"\n--- Chunk {i + 1} ---")
    print(doc.page_content)


hyde_response = document_chain.invoke({"context": hyde_docs, "input": question})
print("HYDE:\n", hyde_response)