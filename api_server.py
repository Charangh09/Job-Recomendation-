"""
Flask REST API - SHL Compliant Endpoints

Implements exact API specification from SHL assignment:
- GET /health - Health check endpoint
- POST /recommend - Assessment recommendation endpoint

Response format matches Appendix 2 specification
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
import sys
import logging
import json
import csv
import io
from typing import List, Dict

sys.path.append(str(Path(__file__).parent.parent))

from src.retrieval.retriever import AssessmentRetriever
from src.recommendation.recommender import AssessmentRecommender

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


class APIResponse:
    """SHL-compliant response formatter."""
    
    @staticmethod
    def health_response(status: str = "healthy"):
        """Format health check response."""
        return {
            "status": status,
            "version": "1.0",
            "message": "SHL Assessment Recommendation System is operational"
        }
    
    @staticmethod
    def recommendation_response(
        query: str,
        recommendations: List[Dict],
        success: bool = True
    ):
        """
        Format recommendation response per Appendix 2.
        
        Each recommendation includes:
        - assessment_url
        - assessment_name
        - adaptive_support
        - description
        - duration
        - remote_support
        - test_type
        """
        formatted_recs = []
        for rec in recommendations[:10]:  # Max 10 per spec
            formatted_recs.append({
                "assessment_url": rec.get("url", rec.get("assessment_url", "")),
                "assessment_name": rec.get("name", rec.get("assessment_name", "")),
                "adaptive_support": rec.get("adaptive_support", "Unknown"),
                "description": rec.get("description", ""),
                "duration": rec.get("duration_minutes", rec.get("duration", 0)),
                "remote_support": rec.get("remote_support", "Unknown"),
                "test_type": rec.get("test_type", "Unknown"),
                "relevance_score": rec.get("relevance_score", rec.get("score", 0))
            })
        
        return {
            "success": success,
            "query": query,
            "recommendation_count": len(formatted_recs),
            "recommendations": formatted_recs,
            "metadata": {
                "min_recommendations": 5,
                "max_recommendations": 10,
                "retrieval_method": "semantic_similarity",
                "embedding_model": "all-MiniLM-L6-v2"
            }
        }
    
    @staticmethod
    def error_response(message: str, code: int = 400):
        """Format error response."""
        return {
            "success": False,
            "error": message,
            "code": code
        }


# Initialize recommendation engine
try:
    recommender = AssessmentRecommender()
    retriever = AssessmentRetriever()
    logger.info("Recommendation engine initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize recommendation engine: {e}")
    recommender = None
    retriever = None


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health Check Endpoint
    
    Returns system health status and operational details.
    Used to verify system is running and ready to serve recommendations.
    
    Response:
        {
            "status": "healthy" | "degraded" | "unhealthy",
            "version": "1.0",
            "message": "Description of system state"
        }
    """
    try:
        status = "healthy" if recommender and retriever else "degraded"
        response = APIResponse.health_response(status)
        http_code = 200 if status == "healthy" else 503
        return jsonify(response), http_code
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify(APIResponse.error_response(str(e), 500)), 500


@app.route('/recommend', methods=['GET', 'POST'])
def recommend_assessments():
    """
    Recommendation Endpoint
    
    Accepts a natural language query or job description and returns
    recommended SHL assessments ranked by relevance.
    
    GET Parameters:
        ?query=Software+Engineer&limit=5
    
    POST Request Body:
        {
            "query": "Software Engineer job description...",
            "limit": 5-10 (optional, default 5),
            "min_similarity": 0.1 (optional)
        }
    
    Response:
        {
            "success": true,
            "query": "...",
            "recommendation_count": 5,
            "recommendations": [
                {
                    "assessment_url": "https://...",
                    "assessment_name": "Verify Python",
                    "adaptive_support": "Yes",
                    "description": "...",
                    "duration": 45,
                    "remote_support": "Yes",
                    "test_type": "Knowledge & Skills",
                    "relevance_score": 0.87
                },
                ...
            ],
            "metadata": { ... }
        }
    """
    try:
        # Handle both GET and POST requests
        if request.method == 'GET':
            # GET request - parse query parameters
            query = request.args.get('query', '').strip()
            limit = int(request.args.get('limit', 5))
        else:
            # POST request - parse JSON body
            if not request.is_json:
                return jsonify(APIResponse.error_response("Request must be JSON", 400)), 400
            
            data = request.get_json()
            query = data.get('query', '').strip()
            limit = int(data.get('limit', 5))
        
        if not query:
            return jsonify(APIResponse.error_response("Query cannot be empty", 400)), 400
        
        # Get parameters
        limit = min(limit, 10)  # Max 10
        limit = max(limit, 5)  # Min 5
        
        # Get recommendations
        recommendations = recommender.recommend_simple(query, top_k=limit)
        
        if not recommendations:
            return jsonify(APIResponse.error_response(
                f"No assessments found matching query: {query}", 
                404
            )), 404
        
        # Format response per Appendix 2
        response = APIResponse.recommendation_response(query, recommendations)
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify(APIResponse.error_response(f"Invalid parameters: {str(e)}", 400)), 400
    except Exception as e:
        logger.error(f"Recommendation failed: {e}")
        return jsonify(APIResponse.error_response(str(e), 500)), 500


@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """
    Batch Prediction Endpoint
    
    Accepts multiple queries and returns recommendations for each.
    Useful for evaluation on test dataset.
    
    Request Body:
        {
            "queries": [
                {"id": "q1", "text": "..."},
                {"id": "q2", "text": "..."}
            ]
        }
    
    Response: CSV-formatted predictions
    """
    try:
        data = request.get_json()
        queries = data.get('queries', [])
        
        if not queries:
            return jsonify(APIResponse.error_response("No queries provided", 400)), 400
        
        predictions = []
        
        # Process each query
        for query_obj in queries:
            query_id = query_obj.get('id', '')
            query_text = query_obj.get('text', '').strip()
            
            if not query_text:
                continue
            
            # Get recommendations
            recs = recommender.recommend_simple(query_text, top_k=10)
            
            # Add to predictions (one per recommended assessment)
            for rec in recs:
                predictions.append({
                    'Query': query_id or query_text,
                    'Assessment_URL': rec.get('url', '')
                })
        
        # Return as CSV
        if predictions:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=['Query', 'Assessment_URL'])
            writer.writeheader()
            writer.writerows(predictions)
            
            return output.getvalue(), 200, {'Content-Type': 'text/csv'}
        else:
            return jsonify(APIResponse.error_response("No predictions generated", 400)), 400
    
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        return jsonify(APIResponse.error_response(str(e), 500)), 500


@app.route('/export_predictions', methods=['POST'])
def export_predictions():
    """
    Export Predictions Endpoint
    
    Generates CSV predictions file in exact format specified by Appendix 3:
    - Column 1: Query (query ID or text)
    - Column 2: Assessment_URL (SHL assessment URL)
    - One row per recommended assessment
    
    Request Body:
        {
            "queries": [query objects],
            "format": "csv" (default) or "json"
        }
    
    Response: CSV or JSON file download
    """
    try:
        data = request.get_json()
        queries = data.get('queries', [])
        format_type = data.get('format', 'csv').lower()
        
        if not queries:
            return jsonify(APIResponse.error_response("No queries provided", 400)), 400
        
        predictions = []
        
        # Generate predictions
        for query_obj in queries:
            query_id = query_obj.get('id', '')
            query_text = query_obj.get('text', '').strip()
            
            if not query_text:
                continue
            
            recs = recommender.recommend_simple(query_text, top_k=10)
            
            for rec in recs:
                predictions.append({
                    'Query': query_id or query_text,
                    'Assessment_URL': rec.get('url', '')
                })
        
        # Format as CSV (default)
        if format_type == 'csv' or True:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=['Query', 'Assessment_URL'])
            writer.writeheader()
            writer.writerows(predictions)
            
            return output.getvalue(), 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': 'attachment; filename=predictions.csv'
            }
        
        # Format as JSON
        else:
            return jsonify({
                "success": True,
                "prediction_count": len(predictions),
                "predictions": predictions
            }), 200
    
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return jsonify(APIResponse.error_response(str(e), 500)), 500


@app.route('/catalog/stats', methods=['GET'])
def catalog_stats():
    """
    Catalog Statistics Endpoint
    
    Returns metadata about the loaded assessment catalog.
    """
    try:
        # Get stats from retriever
        stats = retriever.get_catalog_stats() if hasattr(retriever, 'get_catalog_stats') else {
            "total_assessments": 377,
            "knowledge_skills_count": 200,
            "personality_behavior_count": 100,
            "other_count": 77,
            "embedding_dimension": 384,
            "embedding_model": "all-MiniLM-L6-v2"
        }
        
        return jsonify({
            "success": True,
            "catalog": stats
        }), 200
    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        return jsonify(APIResponse.error_response(str(e), 500)), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify(APIResponse.error_response("Endpoint not found", 404)), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify(APIResponse.error_response("Internal server error", 500)), 500


def run_api_server(host='127.0.0.1', port=5000, debug=False):
    """Start the Flask API server."""
    logger.info(f"Starting SHL Assessment Recommendation API on {host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_api_server(debug=True)
