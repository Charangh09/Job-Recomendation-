"""
Simple Flask API endpoint for assessment recommendations
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.retrieval.retriever import AssessmentRetriever

app = Flask(__name__)
CORS(app)

# Initialize retriever
retriever = AssessmentRetriever()

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation."""
    return jsonify({
        "message": "SHL Assessment Recommendation API",
        "version": "1.0",
        "endpoints": {
            "/recommend": {
                "method": "GET or POST",
                "description": "Get assessment recommendations",
                "parameters": {
                    "query": "Search query (job title, skills, etc.)",
                    "top_k": "Number of results (default: 5)"
                }
            },
            "/health": {
                "method": "GET",
                "description": "Health check endpoint"
            }
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "SHL Assessment API"})

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Get assessment recommendations based on query."""
    try:
        # Get query from request
        if request.method == 'POST':
            data = request.get_json()
            query = data.get('query', '')
            top_k = int(data.get('top_k', 5))
        else:
            query = request.args.get('query', '')
            top_k = int(request.args.get('top_k', 5))
        
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
        
        # Get recommendations
        results = retriever.search(query, top_k=top_k)
        
        # Format response
        response = {
            "query": query,
            "count": len(results),
            "recommendations": results
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
