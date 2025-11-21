from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# === Config ===
MODEL_NAME = "llama3.2:latest"
EMBED_MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"
COLLECTION = "ollama_vectors"

# === Qdrant client ===
client = QdrantClient(url="http://localhost:6333")

# === Embeddings & VectorStore ===
embeddings = HuggingFaceEmbeddings(
    model_name=EMBED_MODEL_NAME,
    encode_kwargs={'normalize_embeddings': True}  # Add normalization
)
vectorstore = Qdrant(
    client=client,
    collection_name=COLLECTION,
    embeddings=embeddings,
    content_payload_key="page_content",  # Match the expected content key
    metadata_payload_key="metadata",
)

# === LLM ===
llm = Ollama(
    model=MODEL_NAME,
    temperature=0.1,  # Lower temperature for more focused answers
    top_p=0.9,  # More focused token selection
    top_k=10,  # Consider fewer tokens
)

# === Create prompt template ===
prompt = PromptTemplate.from_template("""You are a helpful AI assistant. Below you will find a context and a question. Your task is to:
1. Read the context carefully
2. If you find ANY relevant information in the context that answers the question, even partially, use that information in your answer
3. Give a direct, clear answer using the information found
4. If the context does NOT contain relevant information, just respond with what you knew before context
Context:
{context}

Question: {question}

Instructions for answering:
- If the context contains ANY relevant information, use it to answer
- Answer directly and concisely
- Quote the relevant part of the context if applicable
- Do not say "I don't have enough information" if the context contains relevant information
- Only say "I don't have enough information in my database" if the context is completely unrelated to the question. Then continue answerin with what you already know before context.

Your answer: """)

# === Create chain components ===
def get_context(query):
    try:
        # Get more potential matches with lower threshold
        docs = vectorstore.similarity_search(
            query,
            k=3,  # Keep top 3 most relevant
            score_threshold=0.3  # Lower threshold for better recall
        )
        # Debug print
        print(f"Retrieved {len(docs)} documents")
        for i, doc in enumerate(docs):
            print(f"Document {i + 1}: {doc.page_content}")

        # Ensure we have valid content
        valid_docs = [doc for doc in docs if hasattr(doc, 'page_content') and doc.page_content]
        if not valid_docs:
            print("No valid documents found")
            return "No relevant information found."
        
        # Format context with clear separation and emphasis
        context_parts = []
        for i, doc in enumerate(valid_docs, 1):
            context_parts.append(f"Relevant Information #{i}:\n{doc.page_content}")
        
        context = "\n\n".join(context_parts)
        print(f"Final context: {context}")
        return context
    except Exception as e:
        print(f"Error in get_context: {str(e)}")
        return "Error retrieving information."

def process_input(input_dict):
    if not isinstance(input_dict, dict) or "question" not in input_dict:
        return {"context": "Invalid input", "question": "No question provided"}
    question = input_dict["question"]
    if not isinstance(question, str) or not question.strip():
        return {"context": "Invalid input", "question": "No valid question provided"}
    context = get_context(question)
    return {"context": context or "No context available", "question": question}

# === Create the chain ===
qa_chain = RunnablePassthrough() | process_input | prompt | llm | StrOutputParser()

# === Routes ===
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
def ask(prompt: str = Form(...)):
    try:
        if not prompt or not isinstance(prompt, str):
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid prompt provided"}
            )
        result = qa_chain.invoke({"question": prompt.strip()})
        if not result:
            return JSONResponse(
                status_code=500,
                content={"error": "No response generated"}
            )
        return JSONResponse({"response": result})
    except Exception as e:
        print(f"Error in ask endpoint: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "An error occurred while processing your request"}
        )