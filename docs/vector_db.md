# Using `vector_db.py`

The `vector_db.py` script is responsible for managing the vector database. It provides utilities for interacting with the Qdrant database, such as creating collections, querying data, and managing stored embeddings.

## Step-by-Step Instructions

### 1. Purpose
This script:
- Connects to the Qdrant vector database.
- Allows you to create, delete, or manage collections.
- Provides querying capabilities to retrieve relevant vectors based on input.

### 2. Prerequisites
- Ensure the Qdrant server is running locally or remotely.
- Verify that the `requirements.txt` dependencies are installed.

### 3. How to Use
1. Open a terminal in the project directory.
2. Run the script with the following command:
   ```powershell
   python vector_db.py
   ```
3. Follow the prompts or modify the script to perform specific database operations.

### 4. Configuration
- Update the Qdrant server URL and port in the script if necessary.
- Modify the collection name or other parameters to suit your use case.

### 5. Troubleshooting
- If you encounter connection issues, ensure the Qdrant server is running and accessible.
- Check the logs for any errors during database operations.