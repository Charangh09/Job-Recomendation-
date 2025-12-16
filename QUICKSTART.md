# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key (for LLM-based recommendations)

## Installation

### Option 1: Automated Setup (Recommended)

```bash
python setup_and_run.py
```

Select option 5 for full setup and launch.

### Option 2: Manual Setup

1. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
```
Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_key_here
```

4. **Run data pipeline:**
```bash
# Step 1: Scrape SHL catalog
python src/scraper/scrape_shl.py

# Step 2: Parse and clean data
python src/scraper/parser.py

# Step 3: Build vector database
python src/embeddings/build_vector_db.py
```

5. **Launch application:**
```bash
streamlit run app.py
```

## Usage

### Web Interface

1. Navigate to `http://localhost:8501`
2. Enter job requirements:
   - Job title
   - Required skills (comma-separated)
   - Experience level
   - Additional context (optional)
3. Click "Get Recommendations"
4. Review AI-generated recommendations and detailed assessment information

### Command Line Testing

Test retrieval:
```bash
python src/retrieval/retriever.py
```

Test recommendations:
```bash
python src/recommendation/recommender.py
```

Run evaluation:
```bash
python src/evaluation/evaluate.py
```

## Evaluation

The system includes built-in evaluation metrics:

- **Retrieval Precision**: How many retrieved assessments are relevant
- **Recommendation Relevance**: Quality of recommendations vs. expected results
- **Explanation Quality**: Clarity and usefulness of AI-generated explanations

Run evaluation:
```bash
python src/evaluation/evaluate.py
```

Results are saved to `data/evaluation/evaluation_report.json`

## Troubleshooting

### OpenAI API Errors
- Ensure your API key is correctly set in `.env`
- Check your OpenAI account has available credits
- Use the system without LLM explanations (uncheck the option in UI)

### ChromaDB Errors
- Delete `data/vector_db/` and rebuild: `python src/embeddings/build_vector_db.py`
- Ensure ChromaDB is properly installed: `pip install chromadb --upgrade`

### Model Download Issues
- First run downloads embedding models (~80MB)
- Ensure stable internet connection
- Models are cached in `.cache/` directory

## Project Structure

```
SHL assignment/
├── app.py                  # Streamlit web application
├── config.yaml            # Configuration settings
├── requirements.txt       # Python dependencies
├── setup_and_run.py      # Automated setup script
│
├── src/
│   ├── scraper/          # Web scraping module
│   ├── embeddings/       # Embedding generation
│   ├── retrieval/        # Semantic search
│   ├── recommendation/   # RAG-based recommendations
│   ├── evaluation/       # System evaluation
│   └── utils/           # Utility functions
│
└── data/
    ├── raw/             # Scraped data
    ├── processed/       # Cleaned data
    ├── vector_db/       # ChromaDB storage
    └── evaluation/      # Benchmark data
```

## Next Steps

1. Customize configuration in `config.yaml`
2. Add custom benchmark test cases in `data/evaluation/benchmark_roles.json`
3. Adjust LLM prompts in `config.yaml` for different recommendation styles
4. Extend assessment catalog by modifying `src/scraper/scrape_shl.py`

## Support

For issues or questions:
- Check the main README.md
- Review configuration in config.yaml
- Examine logs for error details
