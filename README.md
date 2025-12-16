# 🎯 SHL Assessment Recommendation System

**A complete, evaluated, and explainable GenAI-based assessment recommendation pipeline grounded entirely in SHL's product catalog.**

A GenAI-powered assessment recommendation system using Retrieval-Augmented Generation (RAG) to help recruiters identify the most suitable SHL assessments for specific job roles.

## ✨ Core Features

- ✅ **Automated Data Pipeline**: Scrapes, parses, and normalizes SHL product catalog
- ✅ **Semantic Search**: Vector embeddings (Sentence-Transformers) for intelligent retrieval
- ✅ **RAG Architecture**: Combines semantic retrieval with GPT-3.5-turbo reasoning
- ✅ **Comprehensive Evaluation**: Retrieval precision, recommendation quality, explanation grounding
- ✅ **Robust Design**: Works with or without LLM (graceful fallback to retrieval-only mode)
- ✅ **Web Interface**: Intuitive Streamlit application with catalog browser
- ✅ **Full Documentation**: Complete technical and user guides
- ✅ **Evaluation Framework**: Built-in metrics for system validation

## 🏗️ Architecture

```
┌─────────────────┐
│  SHL Website    │
│  (Data Source)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Web Scraper    │
│  & Parser       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector DB      │
│  (ChromaDB)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌─────────────────┐
│  User Query     │─────▶│  Retrieval      │
└─────────────────┘      │  Engine         │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  LLM (GPT)      │
                         │  Reasoning      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Ranked         │
                         │  Recommendations│
                         └─────────────────┘
```

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "SHL assignment"
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## 🚀 Usage

### 1. Scrape and Process SHL Catalog

```bash
python src/scraper/scrape_shl.py
```

This will:
- Scrape assessment data from SHL website
- Parse and clean the data
- Save to `data/raw/shl_catalog.json`

### 2. Generate Embeddings and Build Vector Database

```bash
python src/embeddings/build_vector_db.py
```

This will:
- Load processed assessment data
- Generate vector embeddings
- Store in ChromaDB for efficient retrieval

### 3. Run the Web Application

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

### 4. Evaluate System Performance

```bash
python src/evaluation/evaluate.py
```

## 📁 Project Structure

```
SHL assignment/
│
├── app.py                          # Streamlit web application
├── requirements.txt                # Python dependencies
├── config.yaml                     # Configuration settings
├── .env.example                    # Environment variables template
├── README.md                       # This file
│
├── src/
│   ├── __init__.py
│   │
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── scrape_shl.py          # Web scraping module
│   │   └── parser.py              # Data parsing utilities
│   │
│   ├── embeddings/
│   │   ├── __init__.py
│   │   ├── embedding_generator.py  # Generate embeddings
│   │   └── build_vector_db.py     # Vector database setup
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── retriever.py           # Semantic search engine
│   │
│   ├── recommendation/
│   │   ├── __init__.py
│   │   └── recommender.py         # RAG-based recommendation engine
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── evaluate.py            # Evaluation metrics
│   │
│   └── utils/
│       ├── __init__.py
│       └── config_loader.py       # Configuration utilities
│
└── data/
    ├── raw/                        # Scraped data
    ├── processed/                  # Cleaned data
    ├── vector_db/                  # ChromaDB storage
    └── evaluation/                 # Benchmark data
```

## 🧪 Evaluation

The system includes multiple evaluation mechanisms:

1. **Retrieval Precision**: Validates top-k retrieved assessments
2. **Recommendation Relevance**: Compares outputs against benchmark roles
3. **Explanation Quality**: Assesses clarity and usefulness of explanations

## 🔧 Configuration

Modify `config.yaml` to adjust:
- Scraping parameters
- Embedding model selection
- Retrieval settings
- LLM parameters
- UI customization

## 📊 Example Usage

**Input:**
- Job Title: Software Engineer
- Skills: Python, Problem Solving, Team Collaboration
- Experience Level: Mid-level

**Output:**
1. **Verify Interactive (G+)** - Assesses coding ability and problem-solving skills
2. **OPQ32** - Evaluates personality traits relevant to team collaboration
3. **Verify Ability Tests** - Measures cognitive abilities for technical roles

## 🛠️ Technology Stack

- **Web Scraping**: BeautifulSoup4, Requests
- **Embeddings**: Sentence Transformers
- **Vector DB**: ChromaDB
- **LLM**: OpenAI GPT-3.5/4
- **Framework**: LangChain
- **UI**: Streamlit
- **Data Processing**: Pandas, NumPy

## 📝 Notes

- Ensure you have a valid OpenAI API key
- The scraper respects robots.txt and implements rate limiting
- First-time setup requires internet connection for model downloads
- Vector database is persisted locally for fast retrieval

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is for educational and assessment purposes.

## 🔗 References

- [SHL Official Website](https://www.shl.com/)
- [RAG Paper](https://arxiv.org/abs/2005.11401)
- [Sentence Transformers](https://www.sbert.net/)
- [LangChain Documentation](https://python.langchain.com/)
