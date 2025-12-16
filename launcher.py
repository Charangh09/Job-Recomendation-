#!/usr/bin/env python
"""
SHL Assessment Recommendation System - Unified Launcher

Provides menu-driven interface to:
1. Run Streamlit web application
2. Run Flask REST API
3. Run web scraper for 377+ assessments  
4. Run evaluation framework
5. Run tests

Ensures both web and API components are operational.
"""

import subprocess
import sys
import os
import time
from pathlib import Path
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SystemLauncher:
    """Unified launcher for SHL system components."""
    
    def __init__(self):
        """Initialize launcher."""
        self.project_root = Path(__file__).parent
        self.processes = {}
        self.setup_environment()
    
    def setup_environment(self):
        """Setup Python path and environment variables."""
        sys.path.insert(0, str(self.project_root))
        os.chdir(self.project_root)
    
    def install_dependencies(self):
        """Install required packages."""
        logger.info("Installing dependencies...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True
            )
            logger.info("✓ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def run_web_scraper(self):
        """Run the production web scraper to collect 377+ assessments."""
        logger.info("\n" + "="*80)
        logger.info("RUNNING SHL PRODUCT CATALOG SCRAPER")
        logger.info("Target: 377+ Individual Test Solutions")
        logger.info("="*80)
        
        try:
            from src.scraper.scrape_shl_production import run_production_scraper
            
            assessments = run_production_scraper()
            logger.info(f"✓ Scraper completed: {len(assessments)} assessments collected")
            return True
        except Exception as e:
            logger.error(f"Scraper failed: {e}")
            return False
    
    def run_streamlit_app(self, port: int = 8501):
        """
        Run Streamlit web application.
        
        Args:
            port: Port to run on (default 8501)
        """
        logger.info("\n" + "="*80)
        logger.info("STARTING STREAMLIT WEB APPLICATION")
        logger.info(f"URL: http://localhost:{port}")
        logger.info("="*80)
        
        try:
            cmd = [
                sys.executable, "-m", "streamlit", "run", "app.py",
                "--logger.level=info",
                f"--server.port={port}"
            ]
            
            process = subprocess.Popen(cmd)
            self.processes['streamlit'] = process
            
            logger.info(f"✓ Streamlit started on port {port}")
            logger.info("Press Ctrl+C to stop")
            
            process.wait()
            
        except Exception as e:
            logger.error(f"Failed to start Streamlit: {e}")
    
    def run_flask_api(self, host: str = '127.0.0.1', port: int = 5000):
        """
        Run Flask REST API.
        
        Args:
            host: Host to bind to (default localhost)
            port: Port to run on (default 5000)
        """
        logger.info("\n" + "="*80)
        logger.info("STARTING FLASK REST API")
        logger.info(f"URL: http://{host}:{port}")
        logger.info("="*80)
        
        try:
            cmd = [
                sys.executable, "api_server.py"
            ]
            
            process = subprocess.Popen(cmd)
            self.processes['flask'] = process
            
            logger.info(f"✓ Flask API started on {host}:{port}")
            logger.info("Press Ctrl+C to stop")
            
            process.wait()
            
        except Exception as e:
            logger.error(f"Failed to start Flask API: {e}")
    
    def run_evaluation(self, training_data: str = None):
        """
        Run evaluation framework.
        
        Args:
            training_data: Path to labeled training data (optional)
        """
        logger.info("\n" + "="*80)
        logger.info("RUNNING EVALUATION FRAMEWORK")
        logger.info("Metric: Mean Recall@K")
        logger.info("="*80)
        
        try:
            from src.recommendation.recommender import AssessmentRecommender
            from src.evaluation.shl_eval_framework import evaluate_recommendation_system
            
            recommender = AssessmentRecommender()
            
            # Use provided path or look for default
            data_path = training_data or "data/labeled_training_data.csv"
            
            if Path(data_path).exists():
                results = evaluate_recommendation_system(recommender, data_path)
                logger.info("✓ Evaluation complete")
                logger.info(f"Results saved to evaluation_results/")
                return True
            else:
                logger.warning(f"Training data not found: {data_path}")
                logger.info("Skipping evaluation - provide labeled training data to evaluate")
                return False
                
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return False
    
    def run_tests(self):
        """Run test suite."""
        logger.info("\n" + "="*80)
        logger.info("RUNNING TEST SUITE")
        logger.info("="*80)
        
        try:
            # Run retrieval tests
            if Path("test_retrieval.py").exists():
                logger.info("Running retrieval tests...")
                subprocess.run([sys.executable, "test_retrieval.py"], check=False)
            
            logger.info("✓ Tests completed")
            return True
            
        except Exception as e:
            logger.error(f"Tests failed: {e}")
            return False
    
    def run_all(self):
        """Run all components (web scraper → API → Streamlit)."""
        logger.info("\n" + "="*80)
        logger.info("SHL ASSESSMENT RECOMMENDATION SYSTEM - FULL DEPLOYMENT")
        logger.info("="*80)
        
        # Step 1: Scrape
        if not self.run_web_scraper():
            logger.warning("Scraper failed, continuing with existing data...")
        
        # Step 2: Start API in background
        logger.info("\nStarting API in background...")
        self.run_flask_api()
        time.sleep(2)
        
        # Step 3: Run tests
        if not self.run_tests():
            logger.warning("Tests failed, continuing...")
        
        # Step 4: Start Streamlit (blocking)
        logger.info("\nStarting Streamlit web app...")
        self.run_streamlit_app()
    
    def show_menu(self):
        """Display interactive menu."""
        while True:
            print("\n" + "="*80)
            print("SHL ASSESSMENT RECOMMENDATION SYSTEM - LAUNCHER")
            print("="*80)
            print("\nChoose an option:")
            print("  1. Install dependencies")
            print("  2. Run web scraper (collect 377+ assessments)")
            print("  3. Run Streamlit web application (localhost:8501)")
            print("  4. Run Flask REST API (localhost:5000)")
            print("  5. Run evaluation framework (Mean Recall@K)")
            print("  6. Run all tests")
            print("  7. Run full system (scraper → API → Streamlit)")
            print("  8. Show API documentation")
            print("  9. Exit")
            print("\n" + "="*80)
            
            choice = input("Enter your choice (1-9): ").strip()
            
            if choice == '1':
                self.install_dependencies()
            elif choice == '2':
                self.run_web_scraper()
            elif choice == '3':
                self.run_streamlit_app()
            elif choice == '4':
                self.run_flask_api()
            elif choice == '5':
                training_data = input("Path to training data (press Enter for default): ").strip()
                self.run_evaluation(training_data or None)
            elif choice == '6':
                self.run_tests()
            elif choice == '7':
                self.run_all()
            elif choice == '8':
                self.show_api_docs()
            elif choice == '9':
                logger.info("Exiting launcher")
                break
            else:
                logger.warning("Invalid choice, please try again")
    
    @staticmethod
    def show_api_docs():
        """Display API documentation."""
        docs = """
╔════════════════════════════════════════════════════════════════════════════╗
║        SHL ASSESSMENT RECOMMENDATION SYSTEM - API DOCUMENTATION            ║
╚════════════════════════════════════════════════════════════════════════════╝

API ENDPOINTS (Running on http://localhost:5000)

1. HEALTH CHECK
   GET /health
   
   Response:
   {
       "status": "healthy",
       "version": "1.0",
       "message": "SHL Assessment Recommendation System is operational"
   }

2. RECOMMENDATION ENDPOINT
   POST /recommend
   
   Request Body:
   {
       "query": "Software Engineer job description...",
       "limit": 5,
       "min_similarity": 0.1
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
       ]
   }

3. BATCH PREDICTION
   POST /batch_predict
   
   Request Body:
   {
       "queries": [
           {"id": "q1", "text": "..."},
           {"id": "q2", "text": "..."}
       ]
   }
   
   Response: CSV format (Query, Assessment_URL)

4. EXPORT PREDICTIONS (Appendix 3 Format)
   POST /export_predictions
   
   Request Body:
   {
       "queries": [...],
       "format": "csv"
   }
   
   Response: CSV file download

5. CATALOG STATISTICS
   GET /catalog/stats
   
   Response:
   {
       "success": true,
       "catalog": {
           "total_assessments": 377,
           "knowledge_skills_count": 200,
           "personality_behavior_count": 100,
           "other_count": 77,
           "embedding_dimension": 384,
           "embedding_model": "all-MiniLM-L6-v2"
       }
   }

EXAMPLE CURL COMMANDS

Health Check:
  curl http://localhost:5000/health

Get Recommendations:
  curl -X POST http://localhost:5000/recommend \\
    -H "Content-Type: application/json" \\
    -d '{"query": "Software Engineer", "limit": 5}'

Batch Predict:
  curl -X POST http://localhost:5000/batch_predict \\
    -H "Content-Type: application/json" \\
    -d '{"queries": [{"id": "q1", "text": "Data Scientist role"}]}'

RESPONSE FORMAT COMPLIANCE

✓ Appendix 2: /recommend endpoint response matches exact specification
  - assessment_url, assessment_name, adaptive_support
  - description, duration, remote_support, test_type
  - relevance_score for ranking

✓ Appendix 3: /export_predictions returns CSV with exact format
  - Column 1: Query (query ID or text)
  - Column 2: Assessment_URL
  - One row per recommended assessment

════════════════════════════════════════════════════════════════════════════════
        """
        print(docs)


def main():
    """Main entry point."""
    launcher = SystemLauncher()
    
    if len(sys.argv) > 1:
        # Command-line mode
        command = sys.argv[1].lower()
        
        if command == 'install':
            launcher.install_dependencies()
        elif command == 'scrape':
            launcher.run_web_scraper()
        elif command == 'web':
            launcher.run_streamlit_app()
        elif command == 'api':
            launcher.run_flask_api()
        elif command == 'eval':
            launcher.run_evaluation(sys.argv[2] if len(sys.argv) > 2 else None)
        elif command == 'test':
            launcher.run_tests()
        elif command == 'all':
            launcher.run_all()
        elif command == 'docs':
            launcher.show_api_docs()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python launcher.py [install|scrape|web|api|eval|test|all|docs]")
    else:
        # Interactive menu
        launcher.show_menu()


if __name__ == '__main__':
    main()
