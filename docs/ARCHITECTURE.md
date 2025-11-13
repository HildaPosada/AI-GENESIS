# System Architecture

## Overview

The AI Fraud Detection System uses **4 cutting-edge AI technologies** to provide comprehensive fraud detection for financial institutions.

## Technology Stack

### 1. Google Gemini (Multimodal AI)

**Purpose**: Pattern analysis and document verification

**Integration**: `backend/app/services/gemini_service.py`

**Capabilities**:
- Transaction pattern analysis
- Behavioral anomaly detection
- Document fraud detection (invoices, bank statements, IDs)
- Natural language explanations of fraud decisions
- Multimodal analysis (text + images)

**API Used**: Google Generative AI SDK

### 2. Opus (Workflow Automation)

**Purpose**: Automated investigation workflows for regulated banking

**Integration**: `backend/app/services/opus_service.py`

**Capabilities**:
- Automated fraud investigation workflows
- Compliance checks (AML, KYC, BSA, OFAC)
- Case routing and prioritization
- Document verification workflows
- Regulatory reporting

**Features**:
- Multi-step workflows
- Manual review checkpoints
- Compliance framework integration
- Priority-based processing

### 3. Qdrant (Vector Database)

**Purpose**: Similarity search for fraud pattern matching

**Integration**: `backend/app/services/qdrant_service.py`

**Capabilities**:
- Store historical fraud patterns as vectors
- Semantic similarity search
- Real-time pattern matching
- Fraud case clustering
- Anomaly detection

**Vector Size**: 384 dimensions
**Distance Metric**: Cosine similarity

### 4. AI/ML API (Multi-Model Access)

**Purpose**: Ensemble fraud detection using multiple AI models

**Integration**: `backend/app/services/aiml_service.py`

**Capabilities**:
- Access to 100+ AI models
- Ensemble decision making
- Model comparison and voting
- Text embedding generation
- Multi-model consensus

**Models Used**:
- GPT-4 (OpenAI)
- Claude 3 Opus (Anthropic)
- LLama 3 (Meta)
- Qwen (Alibaba)

## System Flow

```
┌─────────────────┐
│   Transaction   │
│     Input       │
└────────┬────────┘
         │
         v
┌─────────────────────────────────────────────┐
│     Fraud Detection Engine                  │
│                                             │
│  1. Multi-Model Analysis (AI/ML API)       │
│     ├─ GPT-4 Analysis                      │
│     ├─ Claude Analysis                     │
│     └─ LLama Analysis                      │
│                                             │
│  2. Pattern Analysis (Gemini)              │
│     ├─ Historical comparison               │
│     ├─ Behavioral anomalies                │
│     └─ Risk scoring                        │
│                                             │
│  3. Similarity Search (Qdrant)             │
│     ├─ Generate embedding                  │
│     ├─ Search similar cases                │
│     └─ Pattern matching                    │
│                                             │
│  4. Decision Fusion                        │
│     └─ Combine all analyses                │
└────────┬────────────────────────────────────┘
         │
         v
    Is Fraud?
         │
    ┌────┴────┐
    │         │
   Yes       No
    │         │
    v         v
┌───────┐  ┌─────────┐
│ Opus  │  │ Approve │
│ Auto  │  │ & Log   │
│ Work  │  └─────────┘
│ flow  │
└───┬───┘
    │
    v
Investigation
```

## API Architecture

### Backend (FastAPI)

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── core/
│   │   └── config.py        # Configuration
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   └── services/
│       ├── gemini_service.py     # Google Gemini
│       ├── opus_service.py       # Opus workflows
│       ├── qdrant_service.py     # Qdrant vectors
│       ├── aiml_service.py       # AI/ML API
│       └── fraud_detection_engine.py  # Core engine
```

### Frontend (Web Dashboard)

- **Technology**: HTML + TailwindCSS + Alpine.js
- **Features**:
  - Real-time analysis results
  - Technology breakdown visualization
  - Similar cases display
  - Workflow tracking
  - Risk visualization

## Data Flow

1. **Input**: Transaction or document data
2. **Embedding**: Convert to vector representation
3. **Analysis**: Run through all 4 technologies
4. **Fusion**: Combine results with weighted scoring
5. **Decision**: Determine fraud status
6. **Action**: Create workflow if fraud detected
7. **Storage**: Store case for future matching
8. **Output**: Comprehensive analysis report

## Deployment

### Docker Compose Stack

- **Backend**: FastAPI application (Port 8000)
- **Qdrant**: Vector database (Port 6333)
- **Redis**: Caching layer (Port 6379)
- **Frontend**: Nginx server (Port 3000)

## Security Considerations

- API keys stored in environment variables
- HTTPS in production
- Rate limiting
- Input validation
- SQL injection prevention
- XSS protection

## Scalability

- Horizontal scaling with load balancers
- Qdrant clustering for large datasets
- Redis caching for performance
- Async processing for long-running tasks
- Background workers for workflow processing

## Monitoring

- Health check endpoints
- Service status monitoring
- API usage tracking
- Fraud detection statistics
- Model performance metrics
