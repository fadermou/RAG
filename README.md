# AI Document Assistant - RAG System

A production-ready Retrieval-Augmented Generation (RAG) system built with Django and modern AI technologies. Upload documents, ask questions, and get AI-powered answers grounded in your content.

## 🚀 Features

- **Document Upload & Processing** - Upload PDFs and extract text content
- **Vector-Based Search** - Semantic similarity search using embeddings
- **AI-Powered Answers** - GPT-3.5 generates answers based on document context
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
5. **Generation** → OpenAI GPT-3.5 generates contextual answers

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL (metadata), Qdrant (vectors)
- **AI/ML**: OpenAI GPT-3.5, SentenceTransformers
- **Authentication**: JWT tokens
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Deployment**: Docker, Docker Compose

## 📋 Prerequisites

- Python 3.9+
- Docker & Docker Compose
- OpenAI API key

## ⚡ Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag-document-assistant
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start the services**
   ```bash
   make up
   # or
   docker-compose up --build
   ```

4. **Access the application**
   - Navigate to `http://localhost:8000`
   - Register a new account or login
   - Start uploading documents and asking questions!

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-3.5 | Required |
| `DEBUG` | Django debug mode | `True` |
| `SECRET_KEY` | Django secret key | Auto-generated |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |

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
- **Answer Generation**: OpenAI GPT-3.5 generates grounded responses

## 🔒 Security Features

- JWT-based authentication
- User-scoped document access
- Input validation and sanitization
- CORS protection
- Environment-based configuration

## 📁 Project Structure

```
├── backend/
│   ├── backend/          # Django settings
│   ├── documents/        # Document models
│   ├── users/           # User auth & views
│   └── services/        # RAG pipeline services
├── static/              # CSS & JavaScript
├── docker-compose.yml   # Container orchestration
├── Dockerfile          # Backend container
├── Makefile           # Development commands
└── README.md
```

## 🧪 Testing

Run the test suite:
```bash
docker-compose exec backend python manage.py test
```

## 🚀 Production Deployment

### What I Would Do Next

- **Caching Layer**: Implement Redis for frequent queries and generated answers
- **File Storage**: Move to AWS S3 or similar cloud storage for uploaded files
- **Monitoring**: Add application performance monitoring (APM) and logging
- **Rate Limiting**: Implement API rate limiting for production usage
- **CI/CD Pipeline**: Set up automated testing and deployment workflows

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-3.5 Turbo API
- Qdrant for vector database capabilities
- SentenceTransformers for embedding models
- Django community for the excellent framework

---

**Built with ❤️ for intelligent document processing**