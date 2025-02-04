# Study Session RAG API

A FastAPI-based API for creating and querying document embeddings using RAG (Retrieval Augmented Generation) patterns. The system uses Azure OpenAI for embeddings and LLM capabilities, Weaviate as a vector store, and Temporal.io for handling asynchronous operations.

## Technologies

- **FastAPI**: Modern, fast web framework for building APIs
- **Azure OpenAI**: For embeddings and LLM capabilities
- **Weaviate**: Vector database for storing and querying embeddings
- **Temporal.io**: For handling asynchronous workflow operations
- **Unstructured.io**: For processing and extracting text from various document formats
- **Python 3.12+**: Required for running the application

## Setup

1. Clone the repository
2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -e .
```

4. Copy the environment file and update the values:

```bash
cp .env.dist .env
```

Required environment variables include:

- Azure OpenAI configuration
- Weaviate connection details
- Unstructured.io API credentials
- Temporal.io connection details
- Storage configuration (S3-compatible)

## Running the Application

Start the FastAPI server:

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

For the Temporal worker:

```bash
python src/worker.py
```

## API Endpoints

Please find the OpenAPI docs under `/docs`.

The API provides several endpoints under the `/v1` prefix:

### Query Endpoints

- `POST /v1/query/simple`: Execute a simple RAG query
- `POST /v1/query/agentic`: Execute an agentic RAG query with self-improvement capabilities
- `POST /v1/query/documents`: Retrieve relevant documents for a query

### Embedding Endpoints

- `POST /v1/embed/file`: Create embeddings from a file

## Project Structure

- `src/`: Main application code
  - `main.py`: FastAPI application entry point
  - `routes/`: API route definitions
  - `services/`: Core business logic
  - `jobs/`: Temporal workflows and activities
  - `utils/`: Utility functions and configurations

## Development

The project uses several development tools:

- Ruff for linting and formatting
- Pyright for type checking
- JupyterLab for interactive development

Configure VS Code settings for the best development experience using the provided `.vscode/settings.json`.

## License

Private - Do Not Upload
