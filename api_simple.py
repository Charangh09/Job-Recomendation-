"""
Simple Flask API - Fast Loading Version
Direct retrieval without heavy LLM dependencies
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import sys
import logging

sys.path.append(str(Path(__file__).parent))

from src.retrieval.retriever import AssessmentRetriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS

# Initialize retriever only (faster than full recommender)
try:
    retriever = AssessmentRetriever()
    logger.info("✅ Retrieval engine initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize: {e}")
    retriever = None


@app.route('/', methods=['GET'])
def home():
    """Home page with API documentation."""
    return jsonify({
        "message": "SHL Assessment Recommendation API",
        "version": "1.0",
        "endpoints": {
            "GET /health": "Check API health",
            "GET /recommend?query=text": "Get recommendations (GET)",
            "POST /recommend": "Get recommendations (POST with JSON)"
        },
        "example_get": "http://localhost:5000/recommend?query=Java developer&limit=5",
        "example_post": {
            "url": "http://localhost:5000/recommend",
            "method": "POST",
            "body": {"query": "Java developer", "limit": 5}
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    status = "healthy" if retriever else "unhealthy"
    return jsonify({
        "status": status,
        "version": "1.0",
        "message": "API is running"
    })


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """
    Recommendation endpoint - supports both GET and POST.
    
    GET: /recommend?query=Java+developer&limit=5
    POST: {"query": "Java developer", "limit": 5}
    """
    try:
        # Handle both GET and POST
        if request.method == 'GET':
            query = request.args.get('query', '').strip()
            limit = int(request.args.get('limit', 5))
        else:
            data = request.get_json() or {}
            query = data.get('query', '').strip()
            limit = int(data.get('limit', 5))
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Query parameter is required",
                "example": "?query=Java developer&limit=5"
            }), 400
        
        # Validate limit
        limit = max(5, min(limit, 10))
        
        # Get recommendations
        results = retriever.search(query, top_k=limit)
        
        if not results:
            return jsonify({
                "success": False,
                "error": "No assessments found",
                "query": query
            }), 404
        
        # Format response
        recommendations = []
        for r in results:
            recommendations.append({
                "assessment_name": r.get('name', 'Unknown'),
                "assessment_url": r.get('assessment_url', ''),
                "category": r.get('category', 'Unknown'),
                "description": r.get('description', ''),
                "skills_measured": r.get('skills_measured', ''),
                "job_suitability": r.get('job_suitability', ''),
                "duration": r.get('duration', 'Variable'),
                "relevance_score": round(r.get('score', 0), 4)
            })
        
        return jsonify({
            "success": True,
            "query": query,
            "recommendation_count": len(recommendations),
            "recommendations": recommendations,
            "metadata": {
                "retrieval_method": "semantic_similarity",
                "embedding_model": "all-MiniLM-L6-v2",
                "total_assessments": 65
            }
        })
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    logger.info("🚀 Starting SHL Assessment API on http://localhost:5000")
    logger.info("📖 Visit http://localhost:5000 for API documentation")
    app.run(host='0.0.0.0', port=5000, debug=False)
