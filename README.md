# 🤖 AI-Powered Recruitment Platform

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-FFD21E?style=for-the-badge)](https://huggingface.co/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

> An intelligent recruitment platform that revolutionizes candidate screening using AI-powered semantic matching and Retrieval-Augmented Generation (RAG).

## 🎯 Features

- 🚀 **Smart Resume Matching** - AI-powered job recommendations with similarity scores
- 📄 **Automated Resume Analysis** - Extract skills, experience, and candidate details  
- 🏢 **Job Description Generation** - Create realistic jobs across multiple domains
- 📊 **Analytics Dashboard** - Comprehensive market insights and trends
- 🔍 **Semantic Search** - Advanced vector-based job matching
- 📱 **Responsive Design** - Works on all devices and browsers

## 🛠️ Tech Stack

| **Category** | **Technology** | **Purpose** |
|--------------|----------------|-------------|
| **Frontend** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) | Web interface & UI |
| **Vector DB** | ![Qdrant](https://img.shields.io/badge/Qdrant-DC244C?style=flat&logo=qdrant&logoColor=white) | Semantic search & embeddings |
| **Database** | ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=flat&logo=mongodb&logoColor=white) | Document storage |
| **AI/ML** | ![Groq](https://img.shields.io/badge/Groq-F55036?style=flat) | LLM API integration |
| **Embeddings** | ![Hugging Face](https://img.shields.io/badge/🤗%20HF-FFD21E?style=flat) | Text vectorization |
| **LLM** | ![Llama](https://img.shields.io/badge/Llama-0467DF?style=flat) | Natural language processing |
| **File Processing** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | PDF/DOCX/TXT parsing |

## 🏗️ Architecture

```mermaid
graph TD
    A[User Interface - Streamlit] --> B[Resume Processing Engine]
    B --> C[AI Analysis Layer - Groq/Llama]
    C --> D[Vector Database - Qdrant]
    C --> E[Document Database - MongoDB]
    D --> F[Semantic Search & Matching]
    E --> F
    F --> G[Recommendations & Analytics]
    G --> A
```

## 🚀 Quick Start

### Prerequisites

```bash
# System Requirements
- Python 3.8+
- Modern web browser
- Stable internet connection (min 1 Mbps)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/username/ai-recruitment-platform.git
cd ai-recruitment-platform

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database connections

# Run the application
streamlit run app.py
```

### Environment Variables

```bash
# .env file
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_string
QDRANT_URL=your_qdrant_instance_url
QDRANT_API_KEY=your_qdrant_api_key
HUGGINGFACE_TOKEN=your_hf_token
```

## 📖 Usage

### 1. Upload Resume
```python
# Supported formats: PDF, DOCX, TXT (max 10MB)
uploaded_file = st.file_uploader("Choose a resume file")
```

### 2. Job Management
- **Auto-generate jobs** across 6+ domains
- **Manual job entry** for custom descriptions  
- **Search & filter** existing job database

### 3. Get AI Recommendations
- Upload resume → Process with LLM → Generate vector embeddings
- Semantic search against job database
- Receive ranked matches with similarity scores

### 4. Analytics Dashboard
- Job market insights and trends
- Skills demand analysis
- Geographic distribution
- Company and domain metrics

## 📊 System Workflow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant AI_Engine
    participant Vector_DB
    participant Mongo_DB
    
    User->>Frontend: Upload Resume
    Frontend->>AI_Engine: Process Resume
    AI_Engine->>Vector_DB: Store Embeddings
    User->>Frontend: Request Recommendations
    Frontend->>Vector_DB: Semantic Search
    Vector_DB->>Mongo_DB: Fetch Job Details
    Mongo_DB->>Frontend: Return Matches
    Frontend->>User: Display Recommendations
```

## 🚀 Deployment

### Docker
```bash
# Build image
docker build -t ai-recruitment-platform .

# Run container
docker run -p 8501:8501 ai-recruitment-platform
```

### Streamlit Cloud
1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Large PDF files (>5MB) may take longer to process
- Some DOCX files with complex formatting might not parse correctly
- Rate limiting on Groq API during high usage

## 🔒 Security

- No personal data stored locally
- Encrypted database connections
- API key environment variables
- Session-based resume processing
- GDPR compliant data handling

## 📊 Statistics

![GitHub stars](https://img.shields.io/github/stars/username/ai-recruitment-platform?style=social)
![GitHub forks](https://img.shields.io/github/forks/username/ai-recruitment-platform?style=social)
![GitHub issues](https://img.shields.io/github/issues/username/ai-recruitment-platform)
![GitHub last commit](https://img.shields.io/github/last-commit/username/ai-recruitment-platform)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Valenteno Lenora**
- GitHub: [@username](https://github.com/Nightking-v)
- LinkedIn: [Profile](https://linkedin.com/in/valentenolenora)
- Email: valentenocavlenora@gmail.com

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Groq](https://groq.com/) for lightning-fast LLM inference
- [Qdrant](https://qdrant.tech/) for vector database capabilities
- [Hugging Face](https://huggingface.co/) for embeddings and models
- [MongoDB](https://www.mongodb.com/) for document storage

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ by [Valenteno Lenora](https://github.com/Nightking-v)

[![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io/)
[![Powered by AI](https://img.shields.io/badge/Powered%20by-AI-00D4AA?style=flat)](https://github.com/username/ai-recruitment-platform)

</div>