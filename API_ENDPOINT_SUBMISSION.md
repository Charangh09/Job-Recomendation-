# 🚀 SHL Assessment API - Submission Ready

## API Endpoint for Query-Based JSON Results

### **Main Endpoint: POST /recommend**

**URL**: `http://localhost:5000/recommend`

**Method**: `POST`

**Content-Type**: `application/json`

---

## 📝 Request Format

```json
{
    "query": "Your job description or requirements text here",
    "limit": 5
}
```

### Parameters:
- **query** (required): Natural language text describing job role, skills, or requirements
- **limit** (optional): Number of results to return (5-10, default: 5)

---

## ✅ Response Format (JSON)

```json
{
    "success": true,
    "query": "I need a Java developer with strong problem-solving skills",
    "recommendation_count": 5,
    "recommendations": [
        {
            "assessment_url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
            "assessment_name": "Java 8 New",
            "adaptive_support": "Unknown",
            "description": "I am hiring for Java developers who can also collaborate effectively with my business teams...",
            "duration": "Variable",
            "remote_support": "Online",
            "test_type": "Job-Specific Skills",
            "relevance_score": 0.85
        },
        {
            "assessment_url": "https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level-new/",
            "assessment_name": "Core Java Entry Level New",
            "adaptive_support": "Unknown",
            "description": "Java assessment for entry level developers...",
            "duration": "Variable",
            "remote_support": "Online",
            "test_type": "Job-Specific Skills",
            "relevance_score": 0.82
        }
    ],
    "metadata": {
        "min_recommendations": 5,
        "max_recommendations": 10,
        "retrieval_method": "semantic_similarity",
        "embedding_model": "all-MiniLM-L6-v2"
    }
}
```

---

## 🔧 How to Use

### 1. Start the API Server

```powershell
cd "c:\Users\sirik\OneDrive\Desktop\SHL assignment"
py api_server.py
```

**Server will start at**: `http://localhost:5000`

---

### 2. Query the API

#### **Using PowerShell:**

```powershell
$body = @{
    query = "I need a Python developer for data analysis"
    limit = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/recommend" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

#### **Using curl (Command Prompt):**

```bash
curl -X POST http://localhost:5000/recommend ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"I need a Python developer for data analysis\", \"limit\": 5}"
```

#### **Using Python:**

```python
import requests

url = "http://localhost:5000/recommend"
data = {
    "query": "I need a Python developer for data analysis",
    "limit": 5
}

response = requests.post(url, json=data)
result = response.json()

print(result)
```

#### **Using Postman:**

1. Method: `POST`
2. URL: `http://localhost:5000/recommend`
3. Headers: 
   - Key: `Content-Type`
   - Value: `application/json`
4. Body (raw JSON):
```json
{
    "query": "I need a Python developer for data analysis",
    "limit": 5
}
```

---

## 📋 Example Queries

### Query 1: Java Developer
```json
{
    "query": "I need a Java developer who can collaborate with business teams",
    "limit": 5
}
```

### Query 2: Data Analyst
```json
{
    "query": "Looking for a Senior Data Analyst with SQL and Excel expertise",
    "limit": 5
}
```

### Query 3: Sales Role
```json
{
    "query": "Need to hire graduates for entry-level sales positions",
    "limit": 5
}
```

### Query 4: Technical Role
```json
{
    "query": "Software engineer with Python and problem-solving skills",
    "limit": 5
}
```

---

## 🎯 Additional Endpoints

### Health Check

**GET** `http://localhost:5000/health`

```json
{
    "status": "healthy",
    "version": "1.0",
    "message": "SHL Assessment Recommendation System is operational"
}
```

### Catalog Statistics

**GET** `http://localhost:5000/catalog/stats`

Returns statistics about the loaded assessment catalog.

---

## 🚀 Quick Start for Submission

### Step 1: Start Server
```powershell
py api_server.py
```

### Step 2: Test with Sample Query
```powershell
$body = '{"query": "Java developer with problem-solving skills", "limit": 5}' 
Invoke-RestMethod -Uri "http://localhost:5000/recommend" -Method Post -Body $body -ContentType "application/json"
```

### Step 3: You'll Get JSON Response
The API returns structured JSON with:
- ✅ Assessment recommendations
- ✅ Relevance scores
- ✅ Assessment URLs
- ✅ Descriptions
- ✅ Metadata

---

## 📊 Response Fields Explanation

| Field | Description |
|-------|-------------|
| `success` | Boolean indicating if request was successful |
| `query` | The original query text |
| `recommendation_count` | Number of recommendations returned |
| `recommendations` | Array of recommended assessments |
| `assessment_url` | Direct link to SHL assessment |
| `assessment_name` | Name of the assessment |
| `description` | Assessment description/query context |
| `duration` | Assessment duration |
| `test_type` | Category/type of assessment |
| `relevance_score` | Similarity score (0-1, higher is better) |
| `metadata` | System metadata and configuration |

---

## ✅ What Makes This Submission-Ready

1. **✅ REST API**: Standard HTTP POST endpoint
2. **✅ JSON Input**: Accepts JSON requests
3. **✅ JSON Output**: Returns structured JSON responses
4. **✅ Query-Based**: Works with natural language text
5. **✅ Real Data**: Connected to Gen_AI Dataset (65 assessments)
6. **✅ Semantic Search**: Uses embeddings for intelligent matching
7. **✅ Ranked Results**: Returns most relevant assessments first
8. **✅ Production-Ready**: Error handling, logging, validation

---

## 📝 For Your Submission

**API Endpoint Information:**

- **URL**: `http://localhost:5000/recommend`
- **Method**: POST
- **Input**: JSON with `query` field (text/string)
- **Output**: JSON with ranked assessment recommendations
- **Technology**: Flask REST API + ChromaDB Vector Store + Sentence Transformers
- **Dataset**: 65 assessments from Gen_AI Dataset.xlsx

**Sample cURL Command for Documentation:**
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Python developer for data analysis", "limit": 5}'
```

---

## 🎯 Testing the API

Run this test script:

```powershell
# Test 1: Health check
Invoke-RestMethod -Uri "http://localhost:5000/health" -Method Get

# Test 2: Java developer query
$query1 = @{query="Java developer"; limit=5} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/recommend" -Method Post -Body $query1 -ContentType "application/json"

# Test 3: Data analyst query
$query2 = @{query="Senior Data Analyst with SQL skills"; limit=5} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/recommend" -Method Post -Body $query2 -ContentType "application/json"
```

---

**Ready for Submission! ✅**

Your API accepts text queries and returns JSON results with assessment recommendations.
