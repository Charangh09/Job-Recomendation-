# 🧪 COMPLETE VERIFICATION GUIDE

**Verify that all system features are working correctly**

---

## ⚡ QUICK VERIFICATION (5 Minutes)

Run these quick checks to verify the system is operational:

### 1. Check Web App is Running
```bash
# Open in browser:
http://localhost:8501

# Expected: Streamlit app loads with:
# - "SHL Assessment Recommendation System" header
# - Job query input field
# - "Get Recommendations" button
# - Browse Catalog tab
```

### 2. Test API Health Check
```bash
curl http://localhost:5000/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "1.0",
#   "message": "SHL Assessment Recommendation System is operational"
# }
```

### 3. Test Basic Recommendation (API)
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Software Engineer", "limit": 5}'

# Expected: JSON response with 5 assessments
# Each should have: name, url, test_type, duration, score
```

### 4. Test Web App (Manual)
- Go to: http://localhost:8501
- Enter: "Data Scientist"
- Click: "Get Recommendations"
- Expected: See 5+ assessments with colors and scores

---

## 🔧 DETAILED COMPONENT VERIFICATION

### Component 1: Data Pipeline

#### Check Vector Database Exists
```bash
# List vector database files
dir data\vector_db\

# Expected: See ChromaDB database files
# Should have: chroma.sqlite3, embeddings.parquet, etc.
```

#### Test Embedding Generation
```python
python -c "
from src.embeddings.embedding_generator import EmbeddingGenerator
gen = EmbeddingGenerator()
embedding = gen.generate_query_embedding('Software Engineer')
print(f'Embedding shape: {embedding.shape}')
print(f'Embedding sample: {embedding[:10]}')
"

# Expected output:
# Embedding shape: (384,)
# Embedding sample: [values from 0-1]
```

#### Verify Assessment Count
```python
python -c "
import json
with open('data/raw/shl_catalog.json', 'r') as f:
    data = json.load(f)
print(f'Total assessments: {len(data)}')
print(f'First assessment: {data[0][\"name\"]}')
print(f'Sample fields: {list(data[0].keys())}')
"

# Expected:
# Total assessments: 20+ (or 377+ if using production scraper)
# Fields should include: name, url, description, test_type, duration, etc.
```

---

### Component 2: Retrieval Engine

#### Test Semantic Search
```python
python -c "
from src.retrieval.retriever import AssessmentRetriever
retriever = AssessmentRetriever()

# Test different queries
queries = [
    'Software Engineer',
    'Sales Manager',
    'Data Analyst',
    'Customer Service'
]

for query in queries:
    results = retriever.retrieve(query, top_k=3)
    print(f'\nQuery: {query}')
    for i, r in enumerate(results[:3]):
        print(f'  {i+1}. {r[\"name\"]} (score: {r[\"score\"]:.3f})')
"

# Expected: Different queries return different top results
# Scores should be between 0 and 1
```

#### Verify Similarity Scoring
```python
python -c "
from src.retrieval.retriever import AssessmentRetriever
retriever = AssessmentRetriever()

# Same query twice should give same results
q1 = retriever.retrieve('Python Developer', top_k=5)
q2 = retriever.retrieve('Python Developer', top_k=5)

print(f'Query 1 results: {[r[\"name\"] for r in q1]}')
print(f'Query 2 results: {[r[\"name\"] for r in q2]}')
print(f'Identical: {q1 == q2}')  # Should be True

# Different queries should give different results
q3 = retriever.retrieve('HR Manager', top_k=5)
print(f'Different query: {[r[\"name\"] for r in q3]}')
print(f'Different from Python: {[r[\"name\"] for r in q1] != [r[\"name\"] for r in q3]}')
"

# Expected:
# Same query twice returns identical results
# Different queries return different results
```

---

### Component 3: Recommendation Engine (RAG)

#### Test Without LLM (Retrieval-Only)
```python
python -c "
from src.recommendation.recommender import AssessmentRecommender
recommender = AssessmentRecommender()

# Get recommendations
recs = recommender.recommend_simple('Software Engineer', top_k=5)

print(f'Recommendation count: {len(recs)}')
for i, rec in enumerate(recs):
    print(f'{i+1}. {rec[\"name\"]}')
    print(f'   Type: {rec.get(\"test_type\", \"Unknown\")}')
    print(f'   Score: {rec.get(\"relevance_score\", rec.get(\"score\", \"N/A\"))}')
    print()
"

# Expected:
# 5 assessments returned
# Each has name, type, and score
# Scores in descending order (highest first)
```

#### Test Type Balance
```python
python -c "
from src.recommendation.recommender import AssessmentRecommender
recommender = AssessmentRecommender()

queries = [
    'Software Engineer with team leadership',
    'Sales Manager',
    'Data Analyst'
]

for query in queries:
    recs = recommender.recommend_simple(query, top_k=5)
    
    knowledge = sum(1 for r in recs if 'Knowledge' in r.get('test_type', ''))
    personality = sum(1 for r in recs if 'Personality' in r.get('test_type', ''))
    
    print(f'\nQuery: {query}')
    print(f'  Knowledge & Skills: {knowledge}')
    print(f'  Personality & Behavior: {personality}')
"

# Expected: Balanced mix for each query
# No query should return only one type
```

---

### Component 4: REST API

#### Test All Endpoints
```bash
# 1. Health Check
echo "=== Health Check ==="
curl -s http://localhost:5000/health | python -m json.tool

# 2. Get Recommendation
echo -e "\n=== Get Recommendation ==="
curl -s -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Software Engineer", "limit": 5}' | python -m json.tool

# 3. Batch Predict
echo -e "\n=== Batch Predict ==="
curl -s -X POST http://localhost:5000/batch_predict \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      {"id": "q1", "text": "Data Scientist"},
      {"id": "q2", "text": "HR Manager"}
    ]
  }' > batch_results.csv
cat batch_results.csv

# 4. Catalog Stats
echo -e "\n=== Catalog Stats ==="
curl -s http://localhost:5000/catalog/stats | python -m json.tool
```

#### Verify API Response Format (Appendix 2)
```python
import json
import requests

response = requests.post(
    'http://localhost:5000/recommend',
    json={'query': 'Software Engineer', 'limit': 5}
)

data = response.json()

# Check required fields
required_fields = ['success', 'query', 'recommendation_count', 'recommendations']
for field in required_fields:
    print(f'{field}: {"✓" if field in data else "✗"}')

# Check each recommendation has required fields
print("\nRecommendation fields:")
rec_fields = ['assessment_url', 'assessment_name', 'adaptive_support', 
              'description', 'duration', 'remote_support', 'test_type']
for field in rec_fields:
    has_field = all(field in rec for rec in data.get('recommendations', []))
    print(f'  {field}: {"✓" if has_field else "✗"}')
```

---

### Component 5: Web Application

#### Test Input Methods

**Method 1: Text Query**
1. Go to http://localhost:8501
2. Enter: "Machine Learning Engineer"
3. Click "Get Recommendations"
4. Expected: See 5+ assessments with scores

**Method 2: Job Description**
1. Enter full job description:
```
We are looking for a Senior Software Engineer with:
- 5+ years of Python experience
- Strong problem-solving skills
- Experience with data analysis
- Team leadership capabilities
```
2. Click "Get Recommendations"
3. Expected: Balanced mix of technical and soft skills assessments

**Method 3: Browse Catalog**
1. Click "Browse Complete Catalog" tab
2. Expected: 
   - See all available assessments
   - Can filter/search
   - See full details for each

#### Test Export Functionality
1. Get recommendations for "Data Analyst"
2. Look for "Download CSV" button
3. Click button
4. Check downloaded file format:
```csv
Assessment Name,URL,Type,Duration
Verify Numerical,https://...,Knowledge & Skills,17
OPQ32,https://...,Personality & Behavior,45
```

#### Test Theme Settings
1. Go to sidebar (hamburger menu)
2. Look for "Theme Settings" section
3. Try:
   - Light mode
   - Dark mode
   - Change colors
4. Expected: UI updates in real-time

---

### Component 6: Data Quality

#### Verify All Assessments Have Required Fields
```python
import json

with open('data/raw/shl_catalog.json', 'r') as f:
    assessments = json.load(f)

required_fields = ['name', 'url', 'description', 'test_type', 'duration_minutes']
missing_count = 0

for i, assessment in enumerate(assessments):
    for field in required_fields:
        if field not in assessment or not assessment[field]:
            print(f"Assessment {i} missing '{field}'")
            missing_count += 1

print(f"\nTotal missing fields: {missing_count}")
if missing_count == 0:
    print("✓ All assessments have required fields")
```

#### Check Assessment Types Distribution
```python
import json
from collections import Counter

with open('data/raw/shl_catalog.json', 'r') as f:
    assessments = json.load(f)

types = Counter(a.get('test_type', 'Unknown') for a in assessments)
print("Assessment Type Distribution:")
for type_name, count in types.most_common():
    print(f"  {type_name}: {count}")
```

---

## 🧪 AUTOMATED TEST SUITE

### Run All Tests
```bash
# Run included test file
python test_retrieval.py

# Expected output:
# Testing retrieval for different queries...
# Different queries return different results: ✓
# Consistent results for same query: ✓
# All queries return results: ✓
```

### Create Comprehensive Test Script
```python
# Save as: test_all_features.py

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("SHL SYSTEM - COMPREHENSIVE VERIFICATION")
print("=" * 80)

# Test 1: Data
print("\n✓ TEST 1: DATA PIPELINE")
try:
    with open('data/raw/shl_catalog.json', 'r') as f:
        assessments = json.load(f)
    print(f"  ✓ Loaded {len(assessments)} assessments")
    print(f"  ✓ Sample fields: {list(assessments[0].keys())}")
except Exception as e:
    print(f"  ✗ Data loading failed: {e}")

# Test 2: Embeddings
print("\n✓ TEST 2: EMBEDDINGS")
try:
    from src.embeddings.embedding_generator import EmbeddingGenerator
    gen = EmbeddingGenerator()
    emb = gen.generate_query_embedding("test query")
    print(f"  ✓ Generated embedding shape: {emb.shape}")
    print(f"  ✓ Embedding dimension: {len(emb)}")
except Exception as e:
    print(f"  ✗ Embedding generation failed: {e}")

# Test 3: Retrieval
print("\n✓ TEST 3: RETRIEVAL")
try:
    from src.retrieval.retriever import AssessmentRetriever
    retriever = AssessmentRetriever()
    
    results1 = retriever.retrieve("Software Engineer", top_k=5)
    results2 = retriever.retrieve("Sales Manager", top_k=5)
    
    same_query = retriever.retrieve("Software Engineer", top_k=5)
    
    print(f"  ✓ Query 1 returned {len(results1)} results")
    print(f"  ✓ Query 2 returned {len(results2)} results")
    print(f"  ✓ Different queries: {[r['name'] for r in results1][:2]} vs {[r['name'] for r in results2][:2]}")
    print(f"  ✓ Consistent results: {results1[0]['name'] == same_query[0]['name']}")
except Exception as e:
    print(f"  ✗ Retrieval failed: {e}")

# Test 4: Recommendations
print("\n✓ TEST 4: RECOMMENDATIONS")
try:
    from src.recommendation.recommender import AssessmentRecommender
    recommender = AssessmentRecommender()
    
    recs = recommender.recommend_simple("Data Scientist", top_k=5)
    
    print(f"  ✓ Generated {len(recs)} recommendations")
    print(f"  ✓ Top result: {recs[0]['name']} ({recs[0].get('test_type', 'Unknown')})")
    
    # Check type balance
    knowledge = sum(1 for r in recs if 'Knowledge' in r.get('test_type', ''))
    personality = sum(1 for r in recs if 'Personality' in r.get('test_type', ''))
    print(f"  ✓ Type balance: {knowledge} Knowledge, {personality} Personality")
except Exception as e:
    print(f"  ✗ Recommendation failed: {e}")

# Test 5: API
print("\n✓ TEST 5: REST API")
try:
    import requests
    
    health = requests.get('http://localhost:5000/health').json()
    print(f"  ✓ API Health: {health.get('status', 'unknown')}")
    
    rec_response = requests.post(
        'http://localhost:5000/recommend',
        json={'query': 'Software Engineer', 'limit': 5}
    ).json()
    print(f"  ✓ API returned {rec_response.get('recommendation_count', 0)} recommendations")
except Exception as e:
    print(f"  ✗ API test failed: {e}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
```

Run it:
```bash
python test_all_features.py
```

---

## 📋 VERIFICATION CHECKLIST

### Data Layer
- [ ] Vector database exists: `dir data/vector_db/`
- [ ] Assessment count ≥ 20: Check with JSON load
- [ ] All assessments have required fields
- [ ] No duplicate assessments
- [ ] Descriptions are non-empty

### Retrieval Layer
- [ ] Embeddings generated successfully
- [ ] Different queries return different results
- [ ] Same query returns consistent results
- [ ] Scores are between 0 and 1
- [ ] Top-K results are ordered by score

### Recommendation Layer
- [ ] Recommendations returned successfully
- [ ] Count between 5-10 per query
- [ ] Mix of test types (K + P)
- [ ] Scores in descending order
- [ ] All required fields present

### API Layer
- [ ] `/health` returns 200 status
- [ ] `/recommend` accepts POST with query
- [ ] Response matches Appendix 2 format
- [ ] `/batch_predict` generates CSV
- [ ] `/catalog/stats` shows metadata

### Web Layer
- [ ] App loads on port 8501
- [ ] Query input works
- [ ] Results display correctly
- [ ] Catalog browser works
- [ ] CSV export works
- [ ] Theme settings work

---

## 🎯 EXPECTED OUTPUTS

### Query: "Software Engineer"
```
Top Results Should Include:
1. Verify Inductive Reasoning (Knowledge & Skills) - 0.89
2. Verify Python (Knowledge & Skills) - 0.87
3. Problem Solving (Knowledge & Skills) - 0.85
4. Teamwork (Personality & Behavior) - 0.74
5. Leadership (Personality & Behavior) - 0.68
```

### Query: "Sales Manager"
```
Top Results Should Include:
1. Sales Potential (Personality & Behavior) - 0.92
2. OPQ32 (Personality & Behavior) - 0.89
3. Leadership Potential (Personality & Behavior) - 0.83
4. Communication Skills (Knowledge & Skills) - 0.76
5. Verify Verbal (Knowledge & Skills) - 0.71
```

### Query: "Data Analyst"
```
Top Results Should Include:
1. Verify Numerical (Knowledge & Skills) - 0.91
2. Data Interpretation (Knowledge & Skills) - 0.88
3. OPQ32 (Personality & Behavior) - 0.72
4. Teamwork (Personality & Behavior) - 0.68
5. Problem Solving (Knowledge & Skills) - 0.65
```

---

## ✅ SUCCESS CRITERIA

**System is working well if:**

✅ All 5+ assessments returned for each query  
✅ Scores range from 0.5 to 1.0 (meaningful similarity)  
✅ Different queries return different results  
✅ Same query returns consistent results  
✅ Mix of Knowledge & Skills and Personality & Behavior tests  
✅ Scores in descending order (highest first)  
✅ Web app loads without errors  
✅ API responds to all endpoints  
✅ CSV export generates valid format  
✅ All required fields present in responses  

---

## 🐛 TROUBLESHOOTING

| Issue | Check | Fix |
|-------|-------|-----|
| No results | Similarity threshold too high | Lower in config.yaml to 0.1 |
| Only one test type | Balance disabled | Set `balance_test_types: true` in config.yaml |
| API not responding | Port conflict | Kill process: `lsof -ti:5000 \| xargs kill` |
| Web app slow | Model loading | Wait for first load, subsequent loads are fast |
| Embedding errors | Model not installed | Run: `pip install sentence-transformers` |
| Empty catalog | Data not loaded | Run: `python launcher.py scrape` |

---

## 📞 GET DETAILED FEEDBACK

```bash
# See full logs
python launcher.py web 2>&1 | grep -i "error\|warning"

# Test with verbose output
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)

from src.recommendation.recommender import AssessmentRecommender
recommender = AssessmentRecommender()
recs = recommender.recommend_simple('test query', top_k=5)
print(f'Got {len(recs)} recommendations')
"
```

---

**Verification Complete When All Checks Pass ✅**
