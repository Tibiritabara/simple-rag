# RAG Application with Python Backend and Next.js Frontend

This is a Retrieval-Augmented Generation (RAG) application that allows users to upload documents and query them using natural language. The application uses Azure OpenAI for embeddings and language model capabilities, with a vector database for efficient document retrieval.

## Architecture

### Backend (Python)

- FastAPI for the REST API
- LangChain and LlamaIndex for RAG capabilities
- Azure OpenAI for embeddings and LLM
- Weaviate as the vector database
- Unstructured.io for document parsing
- Temporal.io for workflow orchestration
- MinIO for object storage
- PostgreSQL for Temporal.io persistence

### Frontend (Next.js)

- Next.js 15.1 with TypeScript
- TailwindCSS for styling
- Dark/Light mode support
- File upload and chat interface

## Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Node.js 18+
- Azure OpenAI API access

## Getting Started

1. First, start the required infrastructure using Docker Compose:

```bash
cd build
docker compose up -d
```

This will start:

- Weaviate (Vector Database) - Port 8081
- Unstructured API (Document Processing) - Port 8800
- PostgreSQL (Database) - Port 5432
- Temporal (Workflow Engine) - Port 7233
- Temporal UI - Port 8233
- MinIO (Object Storage) - Ports 9000, 9001

2. Set up the backend:

```bash
cd backend
```

Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
```

Install dependencies

```bash
uv sync
```

Copy environment file and configure it

```bash
cp .env.dist .env
```

Edit .env with your Azure OpenAI and other credentials

Start the backend server

```bash
python -m uvicorn src.main:app --reload
```

3. Set up the frontend:

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Copy environment file and configure it

```bash
cp .env.dist .env
```

Set NEXT_PUBLIC_BACKEND_URL to your backend URL (default: http://localhost:8000)

Start the development server

```bash
npm run dev
```

4. Access the application:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Temporal UI: http://localhost:8233
- MinIO Console: http://localhost:9001

## Features

- Document Upload: Upload and process various document types
- Two Query Modes:
  - Simple: Direct RAG with Azure OpenAI
  - Agentic: Advanced RAG with multi-step reasoning
- Source Attribution: See which documents were used to answer queries
- Dark/Light Theme Support
- Real-time Chat Interface

## Environment Variables

The application requires several environment variables to be set. Check the following files for required variables:

- Backend: `backend/.env.dist`
- Frontend: `frontend/.env.dist`

## Development

The project uses modern development tools and practices:

- Ruff for Python linting and formatting
- TypeScript for type-safe JavaScript
- TailwindCSS for styling
- Next.js App Router for frontend routing

## License

This project is private and confidential. All rights reserved.
