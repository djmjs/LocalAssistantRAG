# LocalAssistantRAG

On-device RAG assistant — local embeddings + vector DB retrieval for context-aware responses.

A minimal, self-contained example that demonstrates how to:

- Create embeddings from local data
- Store and query embeddings in a local vector store
- Use Retrieval-Augmented Generation (RAG) to answer questions from your data

## Features

- On-device operation (no external persistent cloud required)
- Simple, easy-to-read Python code with a focus on embedders and vector storage
- Ready to extend with different embedding models or vector backends

## Quick start

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the example app:

```powershell
python main.py
```

## Example usage

- `embed_and_store.py` — script to convert local files into embeddings and store them in the included vector data directory.
- `main.py` — small example entrypoint that shows how to query the vector store and produce context-aware responses.

## Repository layout

- `embed_and_store.py` — create embeddings and store them
- `vector_db.py` — vector store wrapper (local file-backed)
- `main.py` — example app / entrypoint
- `requirements.txt` — Python deps
- `qdrant_storage/` — local vector storage (ignored from git large files)

## Contributing

Contributions welcome. If you add features or change behavior, please open a pull request with a short description and tests or examples where appropriate.

## License

This repo previously included an MIT license file. If you want to keep the project licensed, add a `LICENSE` file at the project root.

---

If you want, I can add badges, CI (GitHub Actions) for linting or tests, or an example walkthrough section. Tell me what tone you prefer (developer-focused, tutorial, or README-as-landing-page) and I will adapt the content.
