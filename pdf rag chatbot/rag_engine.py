import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# ================== CONFIG ==================
CHROMA_DB_PATH = os.environ.get("CHROMA_DB_PATH", "/tmp/chroma_db")
os.makedirs(CHROMA_DB_PATH, exist_ok=True)

# Use Groq for LLM (free tier available)
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is required")

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    api_key=groq_api_key,
    temperature=float(os.environ.get("TEMPERATURE", "0.4"))
)

# Use OpenAI embeddings (required for production)
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required for embeddings")

embeddings = OpenAIEmbeddings(api_key=openai_api_key, model="text-embedding-3-small")

print("✅ Using Groq (Mixtral 8x7b) + OpenAI Embeddings")

vectorstore = None

def process_pdf(pdf_path: str):
    global vectorstore
    
    print("📄 Loading PDF...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print("✂️ Splitting document into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=850,
        chunk_overlap=180
    )
    chunks = text_splitter.split_documents(documents)

    print("🔍 Creating vector database...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    print(f"✅ Success! {len(chunks)} chunks created.")
    return len(chunks)


def ask_question(question: str):
    if vectorstore is None:
        return {"answer": "Please upload a PDF first.", "sources": []}

    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    relevant_chunks = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in relevant_chunks])

    prompt = f"""
You are a helpful and accurate assistant. Answer the question based on the provided context from the PDF.

Context:
{context}

Question: {question}

Provide a clear, detailed, and well-structured answer.
If the question is about any Project, explain its Objective, Requirements, and Constraints properly.

Answer:
"""

    response = llm.invoke(prompt)

    sources = []
    for i, doc in enumerate(relevant_chunks, 1):
        page = doc.metadata.get('page', 'Unknown')
        sources.append(f"Page {page + 1}")

    return {
        "answer": response.strip(),
        "sources": sources
    }