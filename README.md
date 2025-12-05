# Step-by-Step Instructions for Setting Up the Project

## Repository layout

- `embed_and_store.py` — create embeddings and store them
- `vector_db.py` — vector store wrapper (local file-backed)
- `main.py` — example app / entrypoint
- `requirements.txt` — Python deps
- `qdrant_storage/` — local vector storage (ignored from git large files)

## Additional Scripts

### `embed_and_store.py`
This script is used to embed data and store it in the Qdrant vector database. Running the following command will be sufficient for this task. For detailed instructions, see [docs/embed_and_store.md](docs/embed_and_store.md)
```powershell
python embed_and_store.py
```

### `vector_db.py`
Additionaly! This script is used to manage the Qdrant vector database, such as creating collections. It is useful for database setup and management tasks. For detailed instructions, see [docs/vector_db.md](docs/vector_db.md).

## 1. Fork and Clone the Repository
1. **Fork the Repository**:  
   - On GitHub, click the "Fork" button to create a copy of the repository under your GitHub account.

2. **Clone the Forked Repository**:  
   - Open a terminal and run:
     ```powershell
     git clone https://github.com/djmjs/LocalAssistantRAG.git
     cd LocalAssistantRAG
     ```

---

## 2. Install Prerequisites
1. **Install Docker**:  
   - Download and install Docker Desktop from [Docker's official site](https://www.docker.com/).

2. **Install Python (if needed)**:  
   - Ensure Python 3.8+ is installed. You can download it from [python.org](https://www.python.org/).

3. **Install `docker-compose` (if not bundled with Docker)**:  
   - Verify `docker-compose` is installed:
     ```powershell
     docker-compose --version
     ```

---

## 3. Set Up the Project
1. **Install Python Dependencies**:  
   - Create a virtual environment and install the required Python packages:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     pip install -r requirements.txt
     ```

2. **Prepare Docker Environment**:  
   - Pull the necessary Docker images defined in `docker-compose.yml`:
   - If you already have these images, skip this step and continue to the next one
     ```powershell
     docker-compose pull
     ```

3. **Start Docker Services**:  
   - Launch the services (e.g., Qdrant) using `docker-compose`:
     ```powershell
     docker-compose up -d
     ollama pull llama3.2
     ```
   - **Note**: Our `docker-compose.yml` file pulls the Ollama image with the latest model, which uses the CPU. If you want to use a GPU, the most straightforward method is to pull the version with ROCm (for AMD GPUs) or CUDA (for NVIDIA GPUs). These will require additional steps whihc I won't cover here.

---

## 4. Verify Qdrant is Running
- Check if Qdrant is running by visiting `http://localhost:6333/dashboard#/collections` in a browser.  
  - If it’s running, you should see the Qdrant confirmation page.

---

## 5. Run the Application
1. **Start the FastAPI Server**:  
   - Run the `main.py` file to start the FastAPI application:
     ```powershell
     python -m uvicorn main:app --host 0.0.0.0 --port 8000
     ```

2. **Access the Application**:  
   - Open a browser and navigate to `http://localhost:8000`.  
   - The homepage (`index.html`) should load.
   - Use the endpoint to send queries to the LLM. 

---

## 6. Test and Modify the Project
1. **Test the LLM Interaction**:  
   - Submit questions to the `/ask` endpoint and verify the responses.

2. **Modify Code**:  
   - Make changes to the codebase (e.g., `main.py`, `embed_and_store.py`, etc.) to customize the behavior.

3. **Commit and Push Changes**:  
   - After making changes, commit and push them to your forked repository:
     ```powershell
     git add .
     git commit -m "Custom changes"
     git push origin main
     ```

---

## 7. Optional: Debugging and Logs
1. **Check Docker Logs**:  
   - If there are issues with Qdrant or other services, check logs:
     ```powershell
     docker-compose logs
     ```

---

## 8. Collaborate and Submit Pull Requests
1. **Sync with Upstream Repository**:  
   - Periodically pull changes from the original repository:
     ```powershell
     git remote add upstream https://github.com/djmjs/LocalAssistantRAG.git
     git fetch upstream
     git merge upstream/main
     ```

2. **Submit Pull Requests**:  
   - Once your changes are ready, submit a pull request to the original repository for review.