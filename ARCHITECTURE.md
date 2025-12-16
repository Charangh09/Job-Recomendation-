# System Architecture Document

## Overview

The SHL Assessment Recommendation System is a GenAI-powered application that uses Retrieval-Augmented Generation (RAG) to recommend suitable SHL assessments for job roles. The system combines semantic search, vector databases, and large language models to provide accurate, explainable recommendations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                      (Streamlit Web App)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RECOMMENDATION ENGINE                          │
│                  (RAG-based Recommender)                         │
│  ┌─────────────────┐          ┌──────────────────┐             │
│  │  Query Builder  │──────────│  LLM Generator   │             │
│  └─────────────────┘          └──────────────────┘             │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RETRIEVAL LAYER                             │
│                 (Semantic Search Engine)                         │
│  ┌──────────────────┐      ┌─────────────────────┐             │
│  │ Embedding        │      │  ChromaDB           │             │
│  │ Generator        │─────▶│  Vector Database    │             │
│  │ (Sentence BERT)  │      │                     │             │
│  └──────────────────┘      └─────────────────────┘             │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │  Raw Data    │──▶│  Processed   │──▶│   Vector     │        │
│  │  (JSON)      │   │  Data (CSV)  │   │  Embeddings  │        │
│  └──────────────┘   └──────────────┘   └──────────────┘        │
└────────────▲───────────────────────────────────────────────────┘
             │
             │
┌────────────┴────────────────────────────────────────────────────┐
│                   DATA INGESTION PIPELINE                        │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │  Web         │──▶│  Parser      │──▶│  Embedding   │        │
│  │  Scraper     │   │  & Cleaner   │   │  Generator   │        │
│  └──────────────┘   └──────────────┘   └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Data Ingestion Pipeline

**Purpose**: Extract, parse, and prepare SHL assessment data

**Components**:
- **Web Scraper** (`src/scraper/scrape_shl.py`)
  - Scrapes SHL product catalog
  - Implements rate limiting and retry logic
  - Outputs structured JSON data
  
- **Data Parser** (`src/scraper/parser.py`)
  - Cleans and normalizes text
  - Creates structured DataFrame
  - Generates full-text representations for embedding

**Data Flow**:
```
SHL Website → Scraper → Raw JSON → Parser → Processed CSV
```

**Key Features**:
- Comprehensive catalog of 20+ SHL assessments
- Structured metadata extraction
- Data validation and cleaning

### 2. Embedding & Vector Database

**Purpose**: Convert text to embeddings for semantic search

**Components**:
- **Embedding Generator** (`src/embeddings/embedding_generator.py`)
  - Uses Sentence Transformers (all-MiniLM-L6-v2)
  - Generates 384-dimensional embeddings
  - Batch processing support
  
- **Vector DB Builder** (`src/embeddings/build_vector_db.py`)
  - Manages ChromaDB persistent storage
  - Indexes assessments by semantic content
  - Supports efficient similarity search

**Technical Details**:
- **Model**: sentence-transformers/all-MiniLM-L6-v2
- **Embedding Dimension**: 384
- **Similarity Metric**: Cosine similarity
- **Storage**: ChromaDB persistent client

### 3. Retrieval Engine

**Purpose**: Find relevant assessments using semantic search

**Components**:
- **Assessment Retriever** (`src/retrieval/retriever.py`)
  - Encodes user queries to embeddings
  - Performs similarity search in vector DB
  - Returns ranked results with scores

**Retrieval Process**:
```
User Query → Embed Query → Search Vector DB → Rank Results → Filter by Threshold
```

**Configuration**:
- Top-K retrieval (default: 5)
- Similarity threshold (default: 0.6)
- Metadata filtering support

### 4. Recommendation Engine (RAG)

**Purpose**: Generate contextualized recommendations with explanations

**Components**:
- **Assessment Recommender** (`src/recommendation/recommender.py`)
  - Combines retrieval with LLM reasoning
  - Generates explanations using GPT-3.5/4
  - Implements RAG pattern

**RAG Pipeline**:
```
1. User Input → Query Construction
2. Query → Retrieval → Top-K Assessments
3. Assessments + Query → LLM Prompt
4. LLM → Generate Recommendations + Explanations
5. Format → Return Results
```

**LLM Integration**:
- **Model**: OpenAI GPT-3.5-turbo (configurable)
- **Temperature**: 0.3 (factual, consistent)
- **Max Tokens**: 1000
- **Grounding**: Only uses retrieved assessments (prevents hallucination)

### 5. Web Interface

**Purpose**: User-friendly interface for recruiters

**Components**:
- **Streamlit App** (`app.py`)
  - Input forms for job requirements
  - Real-time recommendation generation
  - Detailed assessment display
  - Search and browse functionality

**Features**:
- Structured input (job title, skills, experience)
- AI-generated recommendations
- Similarity scores and rankings
- Assessment details with expand/collapse
- CSV export functionality
- Catalog browsing

### 6. Evaluation System

**Purpose**: Validate system effectiveness

**Components**:
- **System Evaluator** (`src/evaluation/evaluate.py`)
  - Benchmark test cases
  - Precision/recall metrics
  - Relevance scoring

**Metrics**:
1. **Retrieval Precision**: Accuracy of retrieved assessments
2. **Recommendation Relevance**: Quality of recommendations
3. **Explanation Quality**: Clarity and usefulness

**Benchmark Coverage**:
- 8 diverse job roles
- Expected assessment mappings
- Experience level variations

## Technology Stack

### Core Technologies

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Web Framework** | Streamlit | User interface |
| **Vector DB** | ChromaDB | Embedding storage & retrieval |
| **Embeddings** | Sentence Transformers | Text-to-vector conversion |
| **LLM** | OpenAI GPT-3.5 | Recommendation generation |
| **Framework** | LangChain | LLM orchestration |
| **Data Processing** | Pandas, NumPy | Data manipulation |
| **Web Scraping** | BeautifulSoup, Requests | Data extraction |

### Model Details

**Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Architecture**: Transformer-based (BERT)
- **Parameters**: 22.7M
- **Dimension**: 384
- **Speed**: ~3000 sentences/sec on CPU
- **Quality**: High for semantic similarity tasks

**LLM**: OpenAI GPT-3.5-turbo
- **Context Window**: 4096 tokens
- **Purpose**: Generate explanations
- **Constraint**: Only uses retrieved context

## Data Flow

### End-to-End Flow

```
1. USER INPUT
   ├─ Job Title: "Software Engineer"
   ├─ Skills: ["Python", "Problem Solving"]
   └─ Experience: "Mid"

2. QUERY CONSTRUCTION
   └─ "Job Title: Software Engineer | Skills: Python, Problem Solving | Experience: Mid"

3. EMBEDDING GENERATION
   └─ [0.23, -0.45, 0.12, ...] (384 dimensions)

4. VECTOR SEARCH
   ├─ Query ChromaDB with embedding
   ├─ Calculate cosine similarities
   └─ Return top-5 matches

5. RETRIEVED ASSESSMENTS
   ├─ Verify Interactive (G+) - 0.85 similarity
   ├─ Verify Inductive Reasoning - 0.82 similarity
   └─ OPQ32 - 0.78 similarity

6. LLM PROMPT CONSTRUCTION
   ├─ System: "You are an HR consultant..."
   ├─ Context: Retrieved assessments
   └─ Task: "Recommend top 3-5 assessments..."

7. LLM GENERATION
   └─ Recommendations with explanations

8. RESPONSE FORMATTING
   ├─ Ranked list
   ├─ Similarity scores
   └─ Detailed information

9. UI DISPLAY
   └─ Rendered in Streamlit
```

## Configuration Management

### config.yaml Structure

```yaml
scraping:
  - URL configuration
  - Retry logic
  - Rate limiting

data_storage:
  - File paths
  - Directory structure

embedding:
  - Model selection
  - Batch size
  - Device (CPU/GPU)

retrieval:
  - Top-K results
  - Similarity threshold
  - Collection name

llm:
  - Model selection
  - Temperature
  - System prompt
  - Token limits

evaluation:
  - Benchmark paths
  - Metrics selection
```

## Security & Privacy

### API Key Management
- Environment variables (.env)
- Never committed to version control
- Local storage only

### Data Privacy
- No external data transmission (except OpenAI API)
- Local vector database
- No user data persistence

## Scalability Considerations

### Current Limitations
- Single-user deployment
- In-memory processing
- Local vector database

### Future Enhancements
1. **Multi-user Support**: Deploy on cloud with authentication
2. **Distributed Vector DB**: Use Pinecone or Weaviate
3. **Caching Layer**: Redis for frequently accessed results
4. **Async Processing**: Background job queues
5. **API Layer**: REST API for integration

## Performance Characteristics

### Latency
- **Embedding Generation**: ~50ms per query
- **Vector Search**: ~10ms for 20 documents
- **LLM Generation**: 2-5 seconds (varies by model)
- **Total End-to-End**: 2-6 seconds

### Resource Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB (including models)
- **Network**: Required for LLM API calls

## Error Handling

### Graceful Degradation
1. **No OpenAI API Key**: System works without LLM explanations
2. **Vector DB Unavailable**: Clear error with setup instructions
3. **No Results**: User-friendly message with suggestions

### Logging
- Structured logging throughout
- Error tracking and debugging
- Performance monitoring

## Testing Strategy

### Unit Tests
- Component-level testing
- Mock external dependencies

### Integration Tests
- End-to-end pipeline testing
- Database connectivity

### Evaluation Tests
- Benchmark-based validation
- Automated metrics calculation

## Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. **Streamlit Cloud**: Direct deployment
2. **Docker**: Containerized deployment
3. **Cloud Platforms**: AWS, GCP, Azure

## Maintenance & Updates

### Regular Tasks
1. Update assessment catalog
2. Rebuild vector database
3. Retrain/update embedding model
4. Refresh benchmark test cases

### Monitoring
- Application logs
- Evaluation metrics
- User feedback

## Conclusion

This architecture provides a robust, scalable foundation for AI-powered assessment recommendations. The RAG approach ensures accuracy by grounding recommendations in the actual catalog, while the modular design allows for easy updates and extensions.
