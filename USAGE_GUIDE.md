# Usage Guide with Examples

## Step-by-Step Usage Instructions

### Initial Setup (One-Time)

```bash
# Step 1: Navigate to project directory
cd "SHL assignment"

# Step 2: Create virtual environment
python -m venv venv

# Step 3: Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here

# Step 6: Run data pipeline
python src/scraper/scrape_shl.py
python src/scraper/parser.py
python src/embeddings/build_vector_db.py

# Step 7: (Optional) Run evaluation
python src/evaluation/evaluate.py
```

### Running the Application

```bash
# Launch the web application
streamlit run app.py

# Access at: http://localhost:8501
```

## Usage Examples

### Example 1: Software Engineering Role

**Input:**
```
Job Title: Senior Software Engineer
Skills: Python, Problem Solving, System Design, Team Leadership
Experience Level: Senior
Additional Context: Need to assess both technical and leadership capabilities
```

**Expected Output:**
1. **Verify Interactive (G+)** (Match: 87%)
   - Assesses problem-solving and analytical thinking
   - Measures numerical and inductive reasoning
   - Perfect for evaluating technical problem-solving
   
2. **Verify Inductive Reasoning** (Match: 85%)
   - Tests pattern recognition and abstract thinking
   - Essential for system design capabilities
   
3. **Leadership Judgment Indicator** (Match: 82%)
   - Evaluates decision-making in complex scenarios
   - Assesses leadership judgment for senior roles

### Example 2: Sales Manager Role

**Input:**
```
Job Title: Sales Manager
Skills: Sales, Leadership, Communication, Negotiation
Experience Level: Senior
Additional Context: B2B software sales, managing a team of 5-10 reps
```

**Expected Output:**
1. **Sales Aptitude Test** (Match: 91%)
   - Direct assessment of sales capabilities
   - Measures persuasion and achievement drive
   
2. **OPQ32** (Match: 88%)
   - Evaluates leadership and interpersonal traits
   - Assesses communication style and influence
   
3. **Leadership Judgment Indicator** (Match: 84%)
   - Tests management decision-making
   - Evaluates strategic thinking

### Example 3: Customer Service Representative

**Input:**
```
Job Title: Customer Service Representative
Skills: Communication, Empathy, Problem Resolution, Patience
Experience Level: Entry
Additional Context: Call center environment, handling customer complaints
```

**Expected Output:**
1. **Customer Contact Styles Questionnaire (CCSQ)** (Match: 93%)
   - Specialized for customer-facing roles
   - Evaluates service orientation and empathy
   
2. **Situational Judgment Test (SJT)** (Match: 87%)
   - Assesses decision-making in customer scenarios
   - Tests conflict resolution skills
   
3. **Workplace English** (Match: 79%)
   - Ensures communication proficiency
   - Evaluates professional language use

### Example 4: Data Analyst

**Input:**
```
Job Title: Data Analyst
Skills: Numerical Analysis, Data Interpretation, Excel, SQL
Experience Level: Mid
```

**Expected Output:**
1. **Verify Numerical Reasoning** (Match: 92%)
   - Direct assessment of numerical skills
   - Tests data interpretation abilities
   
2. **Verify Interactive (G+)** (Match: 86%)
   - Measures analytical thinking
   - Evaluates problem-solving with data
   
3. **Management and Graduate Item Bank** (Match: 81%)
   - Comprehensive cognitive assessment
   - Suitable for analytical roles

## Web Interface Guide

### Main Interface

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 SHL Assessment Recommendation System                    │
│  AI-powered assessment recommendations for your hiring needs │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Get Recommendations] [Browse Catalog]                     │
│                                                              │
│  Enter Job Requirements                                      │
│  ┌────────────────────┐  ┌────────────────────┐           │
│  │ Job Title *        │  │ Required Skills *  │           │
│  │ [____________]     │  │ [____________]     │           │
│  │                    │  │ [____________]     │           │
│  │ Experience Level * │  │ [____________]     │           │
│  │ [▼ Mid       ]     │  │                    │           │
│  └────────────────────┘  └────────────────────┘           │
│                                                              │
│  Additional Context (Optional)                              │
│  ┌──────────────────────────────────────────────┐         │
│  │ [                                             ]│         │
│  └──────────────────────────────────────────────┘         │
│                                                              │
│  ⚙️ Advanced Options                                        │
│  ☑ Use AI-generated explanations                           │
│  ☑ Show similarity scores                                  │
│                                                              │
│  [🚀 Get Recommendations]                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Results Display

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Recommendations                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🤖 AI-Generated Recommendations                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │ Based on your requirements for a Senior Software   │   │
│  │ Engineer, here are my top recommendations:         │   │
│  │                                                     │   │
│  │ 1. Verify Interactive (G+)                         │   │
│  │    This assessment is ideal because...             │   │
│  │                                                     │   │
│  │ 2. OPQ32 (Occupational Personality Questionnaire) │   │
│  │    This will help evaluate...                      │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  📋 Detailed Assessment Information                         │
│  ┌────────────────────────────────────────────────────┐   │
│  │ Verify Interactive (G+)           Match: 87%       │   │
│  │ Category: Cognitive Ability                        │   │
│  │ Duration: 36 minutes                               │   │
│  │ Experience Level: Entry, Mid, Senior               │   │
│  │                                                     │   │
│  │ [📋 Full Details ▼]                                │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  [📥 Download Recommendations (CSV)]                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Command-Line Usage

### Test Individual Components

```bash
# Test web scraper
python src/scraper/scrape_shl.py

# Test data parser
python src/scraper/parser.py

# Test embedding generation
python src/embeddings/embedding_generator.py

# Test vector database
python src/embeddings/build_vector_db.py

# Test retrieval
python src/retrieval/retriever.py

# Test recommendations
python src/recommendation/recommender.py

# Run evaluation
python src/evaluation/evaluate.py
```

### Sample Command-Line Output

```
$ python src/recommendation/recommender.py

INFO - Generating recommendations for: Senior Software Engineer
INFO - Query: Job Title: Senior Software Engineer | Skills: Python, Problem Solving, Team Leadership | Experience: Senior
INFO - Retrieved 5 relevant assessments
INFO - LLM recommendations generated successfully

================================================================================
RECOMMENDATIONS FOR: Senior Software Engineer
================================================================================

Retrieved 5 relevant assessments

--- Top Retrieved Assessments ---

1. Verify Interactive (G+)
   Score: 0.873
   Category: Cognitive Ability

2. Verify Inductive Reasoning
   Score: 0.851
   Category: Cognitive Ability

3. Leadership Judgment Indicator (LJI)
   Score: 0.824
   Category: Leadership Assessment

--- LLM-Generated Recommendations ---

Based on the requirements for a Senior Software Engineer with Python,
Problem Solving, Team Leadership skills, I recommend:

1. Verify Interactive (G+)
   This assessment is highly relevant as it measures problem-solving
   abilities and analytical thinking through interactive tasks...
   [full explanation]

2. Verify Inductive Reasoning
   Essential for evaluating pattern recognition and abstract thinking,
   which are crucial for system design and architecture...
   [full explanation]

3. Leadership Judgment Indicator (LJI)
   For a senior role requiring team leadership, this assessment
   evaluates decision-making quality in complex scenarios...
   [full explanation]
```

## Troubleshooting Common Issues

### Issue 1: OpenAI API Key Error
```
Error: OpenAI API key not found
```

**Solution:**
```bash
# Create .env file
cp .env.example .env

# Edit .env and add:
OPENAI_API_KEY=sk-your-actual-key-here
```

### Issue 2: Vector Database Not Found
```
Error: Vector database not found at data/vector_db
```

**Solution:**
```bash
# Run the complete data pipeline
python src/scraper/scrape_shl.py
python src/scraper/parser.py
python src/embeddings/build_vector_db.py
```

### Issue 3: ChromaDB Import Error
```
ImportError: No module named 'chromadb'
```

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue 4: Model Download Issues
```
Error downloading sentence-transformers model
```

**Solution:**
- Ensure stable internet connection
- First run downloads ~80MB model
- Model cached in `.cache/` directory
- Try: `pip install sentence-transformers --upgrade`

## Best Practices

### For Recruiters

1. **Be Specific**: Provide detailed job requirements for better matches
2. **Use Multiple Skills**: Include 3-5 key skills for comprehensive results
3. **Review Explanations**: Read AI-generated explanations for context
4. **Check Match Scores**: Higher scores indicate better relevance
5. **Export Results**: Download CSV for record-keeping

### For System Administrators

1. **Regular Updates**: Refresh assessment catalog periodically
2. **Monitor Performance**: Check evaluation metrics
3. **Backup Database**: Save vector_db directory
4. **Update Models**: Keep embedding models up-to-date
5. **Log Review**: Check logs for errors or issues

## Advanced Usage

### Custom Benchmarks

Edit `data/evaluation/benchmark_roles.json`:

```json
{
  "id": 9,
  "job_title": "Your Custom Role",
  "skills": ["Skill 1", "Skill 2"],
  "experience_level": "Mid",
  "expected_assessments": [
    "Expected Assessment 1",
    "Expected Assessment 2"
  ]
}
```

Then run evaluation:
```bash
python src/evaluation/evaluate.py
```

### Custom Prompts

Edit `config.yaml`:

```yaml
llm:
  system_prompt: |
    Your custom system prompt here...
    Adjust the tone, style, or focus of recommendations.
```

### Adjust Retrieval Settings

Edit `config.yaml`:

```yaml
retrieval:
  top_k: 10  # Retrieve more results
  similarity_threshold: 0.5  # Lower threshold for more matches
```

## Integration Examples

### Python API Usage

```python
from src.recommendation.recommender import AssessmentRecommender

# Initialize recommender
recommender = AssessmentRecommender()

# Get recommendations
result = recommender.recommend(
    job_title="Data Scientist",
    skills=["Python", "Statistics", "Machine Learning"],
    experience_level="Senior",
    use_llm=True
)

# Access results
for assessment in result['retrieved_assessments']:
    print(f"{assessment['name']}: {assessment['similarity_score']:.2%}")
```

### Batch Processing

```python
import pandas as pd
from src.recommendation.recommender import AssessmentRecommender

# Load job descriptions
jobs_df = pd.read_csv('job_descriptions.csv')

recommender = AssessmentRecommender()
results = []

for _, job in jobs_df.iterrows():
    result = recommender.recommend(
        job_title=job['title'],
        skills=job['skills'].split(','),
        experience_level=job['level']
    )
    results.append({
        'job_title': job['title'],
        'top_assessment': result['retrieved_assessments'][0]['name'],
        'score': result['retrieved_assessments'][0]['similarity_score']
    })

results_df = pd.DataFrame(results)
results_df.to_csv('recommendations_batch.csv', index=False)
```

## Performance Tips

1. **First Run**: Initial model download takes time (~1-2 minutes)
2. **Subsequent Runs**: Much faster with cached models
3. **LLM Calls**: Take 2-5 seconds, can be disabled for faster results
4. **Batch Processing**: Process multiple requests in sequence
5. **Vector DB**: ChromaDB is optimized for fast similarity search

---

**Need Help?**
- Check `README.md` for detailed documentation
- Review `ARCHITECTURE.md` for system design
- See `QUICKSTART.md` for quick setup
- Examine logs for error details
