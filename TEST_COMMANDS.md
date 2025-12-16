# ⚡ QUICK VERIFICATION COMMANDS

Run these commands to verify all features are working:

## 🚀 FASTEST WAY (Automated Test - 2 minutes)

```bash
python verify_system.py
```

This will automatically test:
✓ Data pipeline (vector DB, assessments loaded)
✓ Embeddings (384-d vectors generated)
✓ Retrieval (semantic search working)
✓ Recommendations (RAG pipeline)
✓ REST API (all endpoints)
✓ Web app (Streamlit interface)

Expected output:
```
✓ Data Pipeline - PASS
✓ Embeddings - PASS
✓ Retrieval - PASS
✓ Recommendations - PASS
✓ REST API - PASS
✓ Web App - PASS

✓ ALL TESTS PASSED (6/6)
System is working correctly!
```

---

## 📋 MANUAL VERIFICATION (If you prefer step-by-step)

### 1. Test Vector Database
```bash
python -c "
import json
with open('data/raw/shl_catalog.json') as f:
    data = json.load(f)
print(f'✓ {len(data)} assessments loaded')
"
```

### 2. Test Retrieval
```bash
python -c "
from src.retrieval.retriever import AssessmentRetriever
r = AssessmentRetriever()
results = r.retrieve('Software Engineer', top_k=5)
print(f'✓ Retrieved {len(results)} assessments')
for i, res in enumerate(results, 1):
    print(f'  {i}. {res[\"name\"]}')
"
```

### 3. Test Recommendations
```bash
python -c "
from src.recommendation.recommender import AssessmentRecommender
rec = AssessmentRecommender()
recs = rec.recommend_simple('Data Scientist', top_k=5)
print(f'✓ Generated {len(recs)} recommendations')
for i, r in enumerate(recs, 1):
    print(f'  {i}. {r[\"name\"]} ({r.get(\"test_type\", \"?\")})')
"
```

### 4. Test API
```bash
# Check health
curl http://localhost:5000/health

# Get recommendation
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Software Engineer", "limit": 5}'
```

### 5. Test Web App
```bash
# Open in browser:
http://localhost:8501

# Try:
# 1. Enter "Data Analyst"
# 2. Click "Get Recommendations"
# 3. See results with scores
# 4. Click "Browse Complete Catalog"
# 5. Try "Download CSV"
```

---

## ✅ WHAT SHOULD HAPPEN

### Retrieval Test - Expected Output
```
✓ Retrieved 5 assessments
  1. Verify Inductive Reasoning
  2. Verify Python
  3. Problem Solving
  4. Teamwork Assessment
  5. Leadership Potential
```

### Recommendations Test - Expected Output
```
✓ Generated 5 recommendations
  1. Verify Numerical (Knowledge & Skills)
  2. Data Interpretation (Knowledge & Skills)
  3. OPQ32 (Personality & Behavior)
  4. Teamwork Assessment (Personality & Behavior)
  5. Problem Solving (Knowledge & Skills)
```

### API Health Check - Expected Response
```json
{
  "status": "healthy",
  "version": "1.0",
  "message": "SHL Assessment Recommendation System is operational"
}
```

### API Recommendation - Expected Response
```json
{
  "success": true,
  "query": "Software Engineer",
  "recommendation_count": 5,
  "recommendations": [
    {
      "assessment_name": "Verify Python",
      "assessment_url": "https://www.shl.com/...",
      "test_type": "Knowledge & Skills",
      "duration": 45,
      "adaptive_support": "Yes",
      "remote_support": "Yes",
      "description": "...",
      "relevance_score": 0.87
    },
    ...
  ]
}
```

---

## 🎯 VERIFICATION CHECKLIST

After running `python verify_system.py`, verify:

- [ ] Data Pipeline - PASS (assessments loaded)
- [ ] Embeddings - PASS (vectors generated)
- [ ] Retrieval - PASS (different queries return different results)
- [ ] Recommendations - PASS (balanced K+P types)
- [ ] REST API - PASS (all endpoints responding)
- [ ] Web App - PASS (interface accessible)

**If all pass: ✓ System is working correctly!**

---

## 🐛 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| "No results" | Lower similarity_threshold in config.yaml to 0.1 |
| "API not responding" | Start API: `python api_server.py` |
| "Web app not found" | Start web: `streamlit run app.py` |
| "Embedding error" | Install: `pip install sentence-transformers` |
| "Vector DB not found" | Run: `python launcher.py scrape` |

---

## 📊 COMPREHENSIVE VERIFICATION

For complete testing guide with all features, see:
```
VERIFICATION_GUIDE.md
```

For detailed requirement verification:
```
SHL_IMPLEMENTATION_GUIDE.md
```

---

**Quick Test:** `python verify_system.py` → Should see all PASS ✓
