# AI Document Assistant - RAG System

A production-ready Retrieval-Augmented Generation (RAG) system built with Django and modern AI technologies. Upload documents, ask questions, and get AI-powered answers grounded in your content.

## 🚀 Features

- **Document Upload & Processing** - Upload PDFs and extract text content
- **Vector-Based Search** - Semantic similarity search using embeddings
- **AI-Powered Answers** - OpenAI GPT generates answers based on document context
- **User Authentication** - JWT-based secure login system
- **Modern UI** - Clean, responsive chat interface
- **Multi-Document Support** - Search across all uploaded documents
- **Real-time Processing** - Instant document indexing and query responses

## 🏗️ Architecture

The system follows a modern RAG architecture:

1. **Document Ingestion** → PDF text extraction and chunking
2. **Vector Indexing** → Generate embeddings using SentenceTransformers
3. **Storage** → Metadata in PostgreSQL, vectors in Qdrant
4. **Retrieval** → Semantic search for relevant document chunks
5. **Generation** → OpenAI GPT generates contextual answers

## 🛠️ Tech Stack

- **Backend**: Django REST Framework *(chose over FastAPI for faster development)*
- **Database**: PostgreSQL
- **Vector Database**: Qdrant 
- **AI/ML**: OpenAI GPT, SentenceTransformers
- **Authentication**: JWT tokens
- **Frontend**: HTML5, CSS3, JavaScript 
- **Deployment**: Docker, Docker Compose


## 📋 Prerequisites

- Python 3.9+
- Docker & Docker Compose
- OpenAI API key

## ⚡ Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RAG
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start the services**
   ```bash
   make all     # Start all services with docker-compose up --build
   make clean   # Stop and remove containers with volumes
   make fclean  # Complete cleanup (containers, volumes, system prune)
   make re      # Restart everything (clean + rebuild)
   ```

4. **Access the application**
   - Navigate to `http://localhost:8000/user/login`
   - Register a new account or login
   - Start uploading documents and asking questions!

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT | Required |
| `DEBUG` | Django debug mode | `True` |
| `SECRET_KEY` | Django secret key | Auto-generated |
| `POSTGRES_DB` | Name of the PostgreSQL database | Required |
| `POSTGRES_USER` | PostgreSQL username | Required |
| `POSTGRES_PASSWORD` | PostgreSQL password | Required |
| `POSTGRES_HOST` | PostgreSQL host (e.g., `db` in Docker) | Required |

### Docker Services

- **backend**: Django application server
- **db**: PostgreSQL database
- **qdrant**: Vector database for embeddings

## 🚀 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/user/login/` | POST | User authentication |
| `/user/register/` | POST | User registration |
| `/user/chat/` | POST | Upload documents & ask questions |
| `/user/upload/` | GET | Main chat interface |

## 💡 Usage Examples

### Upload a Document
1. Click the 📎 attachment button
2. Select a PDF file
3. Wait for "Uploaded and processed 1 document(s)" confirmation

### Ask Questions
```
User: "What are the main topics covered in the document?"
AI: "Based on the uploaded document, the main topics include..."

User: "Summarize the key findings"
AI: "The key findings from your document are..."
```

## 🧠 RAG Pipeline Details

### Document Processing
- **Text Extraction**: PyPDF2 extracts text from uploaded PDFs
- **Chunking**: Documents split into 500-word chunks for optimal processing
- **Embedding**: SentenceTransformers converts chunks to 384-dim vectors
- **Storage**: Vectors stored in Qdrant, metadata in PostgreSQL

### Query Processing
- **Embedding**: User questions converted to vectors
- **Similarity Search**: Top-5 most relevant chunks retrieved
- **Context Assembly**: Relevant chunks combined as context
- **Answer Generation**: OpenAI GPT generates grounded responses


## 🔒 Security Features (Implemented / Planned)

### ✅ Implemented
- JWT-based authentication
- User-scoped document access
- Environment-based configuration

### 🔄 In Progress
- Input validation (file type checking, PDF text cleaning for database compatibility)

### 📋 Planned
- CORS protection
- Enhanced input sanitization

## 📁 Project Structure

```
project/
├── backend/             # Django settings & config
├── documents/           # Document models & management
├── users/              # Authentication, chat views, static files & templates
├── uploads/            # User uploaded files
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── init_qdrant.py     # Qdrant initialization script
├── Dockerfile         # Backend container
└── db.sqlite3         # SQLite database (development)

```


## 🚀 Production Deployment

### What I Would Do Next

- **Caching Layer**: Implement Redis for frequent queries and generated answers
- **File Storage**: Move to AWS S3 or similar cloud storage for uploaded files
- **Monitoring**: Add application performance monitoring (APM) and logging
- **Rate Limiting**: Implement API rate limiting for production usage
- **CI/CD Pipeline**: Set up automated testing and deployment workflows


## 🙏 Acknowledgments

- OpenAI for GPT Turbo API
- Qdrant for vector database capabilities
- SentenceTransformers for embedding models
- Django community for the excellent framework

## 📺 Demo Video
The demo.mov file is too large to host on GitHub. You can download it here: [demo.mov](https://drive.google.com/drive/folders/1PJJwJxrH40OpxudnMW684nPwcu_YQxzC)

---

**Built with ❤️ for intelligent document processing**