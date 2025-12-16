#!/usr/bin/env python
"""
Quick Verification Script - Test All System Features

Runs automated tests to verify all components are working correctly.
Execute with: python verify_system.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.RESET}\n")

def print_pass(text):
    """Print passing test"""
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")

def print_fail(text):
    """Print failing test"""
    print(f"{Colors.RED}✗{Colors.RESET} {text}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {text}")

def test_data_pipeline():
    """Test 1: Data Pipeline"""
    print_header("TEST 1: DATA PIPELINE")
    
    try:
        # Check file exists
        catalog_file = Path("data/raw/shl_catalog.json")
        if not catalog_file.exists():
            print_fail("Catalog file not found")
            return False
        
        print_pass("Catalog file exists")
        
        # Load and verify
        with open(catalog_file, 'r', encoding='utf-8') as f:
            assessments = json.load(f)
        
        print_pass(f"Loaded {len(assessments)} assessments")
        
        # Check required fields
        required_fields = ['name', 'description', 'test_type', 'duration_minutes']
        sample = assessments[0]
        
        for field in required_fields:
            if field not in sample:
                print_fail(f"Missing field: {field}")
                return False
        
        print_pass("All required fields present in assessments")
        
        # Check field values
        print_info(f"Sample assessment: {sample['name']}")
        print_info(f"  Test Type: {sample.get('test_type', 'Unknown')}")
        print_info(f"  Duration: {sample.get('duration_minutes', 'N/A')} min")
        
        return True
        
    except Exception as e:
        print_fail(f"Data pipeline test failed: {e}")
        return False

def test_embeddings():
    """Test 2: Embedding Generation"""
    print_header("TEST 2: EMBEDDING GENERATION")
    
    try:
        from src.embeddings.embedding_generator import EmbeddingGenerator
        
        print_info("Initializing embedding generator...")
        gen = EmbeddingGenerator()
        print_pass("Embedding generator initialized")
        
        # Generate embedding
        test_query = "Software Engineer with Python"
        embedding = gen.generate_query_embedding(test_query)
        
        print_pass(f"Generated embedding for: '{test_query}'")
        print_info(f"  Embedding shape: {embedding.shape}")
        print_info(f"  Embedding dimension: {len(embedding)}")
        print_info(f"  Sample values: {embedding[:5]}")
        
        # Verify dimension
        if len(embedding) != 384:
            print_fail(f"Unexpected embedding dimension: {len(embedding)} (expected 384)")
            return False
        
        print_pass("Embedding dimension correct (384)")
        
        return True
        
    except Exception as e:
        print_fail(f"Embedding test failed: {e}")
        return False

def test_retrieval():
    """Test 3: Semantic Retrieval"""
    print_header("TEST 3: SEMANTIC RETRIEVAL")
    
    try:
        from src.retrieval.retriever import AssessmentRetriever
        
        print_info("Initializing retriever...")
        retriever = AssessmentRetriever()
        print_pass("Retriever initialized")
        
        # Test Query 1
        query1 = "Software Engineer"
        results1 = retriever.retrieve(query1, top_k=5)
        print_pass(f"Query 1 ({query1}): {len(results1)} results")
        
        if len(results1) == 0:
            print_fail("No results returned")
            return False
        
        for i, r in enumerate(results1[:3], 1):
            print_info(f"  {i}. {r['name']} (score: {r.get('score', r.get('relevance_score', 0)):.3f})")
        
        # Test Query 2 (different)
        query2 = "Sales Manager"
        results2 = retriever.retrieve(query2, top_k=5)
        print_pass(f"Query 2 ({query2}): {len(results2)} results")
        
        for i, r in enumerate(results2[:3], 1):
            print_info(f"  {i}. {r['name']} (score: {r.get('score', r.get('relevance_score', 0)):.3f})")
        
        # Verify different queries return different results
        names1 = {r['name'] for r in results1}
        names2 = {r['name'] for r in results2}
        
        if names1 == names2:
            print_fail("Different queries returned identical results")
            return False
        
        print_pass("Different queries return different results")
        
        # Verify consistency
        results1_again = retriever.retrieve(query1, top_k=5)
        names1_again = {r['name'] for r in results1_again}
        
        if names1 != names1_again:
            print_fail("Same query returned inconsistent results")
            return False
        
        print_pass("Same query returns consistent results")
        
        return True
        
    except Exception as e:
        print_fail(f"Retrieval test failed: {e}")
        return False

def test_recommendations():
    """Test 4: Recommendation Generation"""
    print_header("TEST 4: RECOMMENDATION GENERATION")
    
    try:
        from src.recommendation.recommender import AssessmentRecommender
        
        print_info("Initializing recommender...")
        recommender = AssessmentRecommender()
        print_pass("Recommender initialized")
        
        # Generate recommendations
        query = "Data Scientist with machine learning focus"
        recommendations = recommender.recommend_simple(query, top_k=5)
        
        if not recommendations:
            print_fail("No recommendations generated")
            return False
        
        print_pass(f"Generated {len(recommendations)} recommendations for: '{query}'")
        
        # Display results
        for i, rec in enumerate(recommendations[:5], 1):
            score = rec.get('relevance_score', rec.get('score', 0))
            test_type = rec.get('test_type', 'Unknown')
            print_info(f"  {i}. {rec['name']} ({test_type}) - {score:.3f}")
        
        # Check type balance
        knowledge_count = sum(1 for r in recommendations if 'Knowledge' in r.get('test_type', ''))
        personality_count = sum(1 for r in recommendations if 'Personality' in r.get('test_type', ''))
        
        print_pass(f"Type distribution: {knowledge_count} Knowledge, {personality_count} Personality")
        
        if knowledge_count == 0 or personality_count == 0:
            print_info("  (Note: Single-type results are normal for some queries)")
        
        # Check scores are in descending order
        scores = [rec.get('relevance_score', rec.get('score', 0)) for rec in recommendations]
        if scores == sorted(scores, reverse=True):
            print_pass("Scores in descending order")
        else:
            print_fail("Scores not properly ordered")
            return False
        
        return True
        
    except Exception as e:
        print_fail(f"Recommendation test failed: {e}")
        return False

def test_api():
    """Test 5: REST API"""
    print_header("TEST 5: REST API ENDPOINTS")
    
    try:
        import requests
        
        # Test Health Check
        print_info("Testing GET /health...")
        try:
            health = requests.get('http://localhost:5000/health', timeout=5).json()
            status = health.get('status', 'unknown')
            print_pass(f"Health check: {status}")
        except requests.ConnectionError:
            print_fail("API not responding on port 5000")
            print_info("  Make sure API is running: python api_server.py")
            return False
        
        # Test Recommendation Endpoint
        print_info("Testing POST /recommend...")
        rec_response = requests.post(
            'http://localhost:5000/recommend',
            json={'query': 'Software Engineer', 'limit': 5},
            timeout=10
        ).json()
        
        if not rec_response.get('success'):
            print_fail("Recommendation endpoint failed")
            return False
        
        count = rec_response.get('recommendation_count', 0)
        print_pass(f"Received {count} recommendations via API")
        
        # Check format
        if 'recommendations' in rec_response:
            rec = rec_response['recommendations'][0]
            required_fields = ['assessment_name', 'assessment_url', 'test_type']
            
            for field in required_fields:
                if field not in rec:
                    print_fail(f"Missing field in recommendation: {field}")
                    return False
            
            print_pass("API response format correct (Appendix 2 compliant)")
        
        # Test Catalog Stats
        print_info("Testing GET /catalog/stats...")
        stats = requests.get('http://localhost:5000/catalog/stats', timeout=5).json()
        total = stats.get('catalog', {}).get('total_assessments', 0)
        print_pass(f"Catalog has {total} assessments")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print_fail("API not accessible")
        print_info("  Start API with: python api_server.py")
        return False
    except Exception as e:
        print_fail(f"API test failed: {e}")
        return False

def test_web_app():
    """Test 6: Web Application"""
    print_header("TEST 6: WEB APPLICATION")
    
    try:
        import requests
        
        print_info("Testing Streamlit app on port 8501...")
        try:
            response = requests.get('http://localhost:8501', timeout=5)
            if response.status_code == 200:
                print_pass("Streamlit app is running")
                return True
            else:
                print_fail(f"Unexpected status code: {response.status_code}")
                return False
        except requests.ConnectionError:
            print_fail("Streamlit app not accessible on port 8501")
            print_info("  Start app with: streamlit run app.py")
            return False
        
    except Exception as e:
        print_fail(f"Web app test failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}SHL SYSTEM VERIFICATION{Colors.RESET}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Run tests
    results = {
        'Data Pipeline': test_data_pipeline(),
        'Embeddings': test_embeddings(),
        'Retrieval': test_retrieval(),
        'Recommendations': test_recommendations(),
        'REST API': test_api(),
        'Web App': test_web_app(),
    }
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if result else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"{status} - {test}")
    
    print()
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED ({passed}/{total}){Colors.RESET}")
        print(f"\n{Colors.GREEN}System is working correctly!{Colors.RESET}\n")
        return 0
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ {passed}/{total} tests passed{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Check failed tests above for details{Colors.RESET}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
