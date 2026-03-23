# AI FactGuard Studio

> **A GenAI Platform for Combating Misinformation and Deepfakes**

AI FactGuard Studio is a comprehensive multimodal AI system that verifies text, image, video, and audio content for misinformation and deepfake manipulation. Built for journalists, newsrooms, media organizations, and content creators.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-14-black.svg)

## ✨ Features

### 🔍 Multimodal Analysis
- **Text Analysis**: Claim extraction and fact-checking
- **Image Detection**: Deepfake and manipulation detection with EXIF analysis
- **Video Analysis**: Frame-by-frame deepfake detection
- **Audio Processing**: Synthetic voice detection (planned)
- **URL Support**: Analyze content from web sources

### 🤖 AI-Powered Detection
- **Deepfake Detection**: CNN-based model detecting face swaps, GAN artifacts, lip-sync mismatch
- **Fact Checking**: RAG pipeline with semantic search and evidence retrieval
- **Multimodal LLM**: Google Gemini API integration for comprehensive analysis
- **Confidence Scoring**: 0-100% confidence levels for all detections

### 📊 Explainable AI
- Human-readable explanations for all decisions
- Feature importance visualization
- Source references and evidence links
- Risk level assessment (Low/Medium/High/Critical)

### 👥 Human-in-the-Loop Workflow
- Review queue for flagged content
- Approve/Reject/Flag actions
- Reviewer feedback logging
- Model improvement tracking

### 🔐 Content Provenance
- SHA-256 digital fingerprints
- EXIF metadata extraction
- Edit history tracking
- Authenticity certificates

### 📈 Analytics Dashboard
- Real-time performance metrics
- Accuracy, Precision, Recall, F1 Score
- Trend analysis and visualization
- Human agreement rate tracking

## 🏗️ Architecture

```
┌─────────────┐
│  Next.js    │
│  Frontend   │
└──────┬──────┘
       │
┌──────▼──────┐
│   FastAPI   │
│   Gateway   │
└──────┬──────┘
       │
   ┌───┴────┬────────┬──────────┐
   │        │        │          │
┌──▼──┐ ┌──▼──┐ ┌───▼───┐ ┌───▼────┐
│Media│ │Fact │ │Review │ │Explain │
│Svc  │ │Check│ │Svc    │ │Engine  │
└──┬──┘ └──┬──┘ └───┬───┘ └────────┘
   │       │        │
┌──▼───────▼────────▼──┐
│  PostgreSQL + Vector │
└──────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- (Optional) Docker & Docker Compose

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd ai-factguard-studio

# Copy environment file
cp .env.example .env
# Edit .env and add your API keys

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Option 2: Manual Setup

**Backend Setup:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
# Create PostgreSQL database 'factguard_db'
# Update DATABASE_URL in .env

# Run server
python -m uvicorn app.main:app --reload
```

**Frontend Setup:**
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📝 Configuration

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://factguard:factguard@localhost:5432/factguard_db

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here  # Optional

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Getting API Keys

1. **Google Gemini API**: [Get API Key](https://makersuite.google.com/app/apikey)
2. **Pinecone** (Optional): [Sign up](https://www.pinecone.io/) - Can use local FAISS as alternative

## 📚 Usage

1. **Analyze Content**
   - Navigate to "Analyze" page
   - Upload file, paste text, or enter URL
   - View real-time analysis results

2. **Review Queue**
   - Check flagged high-risk content
   - Approve or reject AI decisions
   - Provide feedback for model improvement

3. **Analytics**
   - Monitor performance metrics
   - View trend graphs
   - Track accuracy and agreement rates

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL + SQLAlchemy
- **AI/ML**: 
  - Google Gemini API (multimodal analysis)
  - PyTorch (deepfake detection)
  - Sentence Transformers (embeddings)
  - Pinecone/FAISS (vector storage)

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React

## 📖 API Documentation

See [API_DOCUMENTATION.md](./docs/API_DOCUMENTATION.md) for full API reference.

### Key Endpoints

- `POST /api/analyze/upload` - Upload and analyze content
- `GET /api/analyze/{id}` - Get analysis results
- `GET /api/review/queue` - Get review queue
- `POST /api/review/{id}/approve` - Approve analysis
- `GET /api/analytics/overview` - Dashboard metrics

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test
```

## 📦 Deployment

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed deployment instructions.

### Google Cloud Run
```bash
# Build and deploy backend
gcloud run deploy factguard-api --source ./backend

# Build and deploy frontend
gcloud run deploy factguard-app --source ./frontend
```

## 🔮 Future Enhancements

- [ ] Browser extension for real-time fact-checking
- [ ] CMS plugins (WordPress, Drupal)
- [ ] Multilingual support
- [ ] Advanced audio deepfake detection
- [ ] Blockchain-based content verification
- [ ] Mobile applications

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Authors

Built with ❤️ for combating misinformation

## 🙏 Acknowledgments

- Google Gemini API for multimodal AI capabilities
- Open-source ML community
- Journalists and fact-checkers worldwide
