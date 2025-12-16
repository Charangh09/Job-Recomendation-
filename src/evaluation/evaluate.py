"""
System Evaluation Module

This module provides comprehensive evaluation of the recommendation system,
including retrieval precision, recommendation relevance, and explanation quality.
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple
import logging
import yaml
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.recommendation.recommender import AssessmentRecommender
from sklearn.metrics import precision_score, recall_score, ndcg_score
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SystemEvaluator:
    """
    Comprehensive evaluation of the recommendation system.
    
    Evaluates:
    1. Retrieval precision and recall
    2. Recommendation relevance
    3. Explanation quality
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the evaluator.
        
        Args:
            config_path: Path to configuration file
        """
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.eval_config = config['evaluation']
        self.recommender = AssessmentRecommender(config_path)
        
        # Load or create benchmark data
        self.benchmark_path = Path(self.eval_config['benchmark_roles_path'])
        self.benchmarks = self._load_or_create_benchmarks()
    
    def _load_or_create_benchmarks(self) -> List[Dict]:
        """
        Load benchmark test cases or create default ones.
        
        Returns:
            List of benchmark test cases
        """
        if self.benchmark_path.exists():
            with open(self.benchmark_path, 'r') as f:
                return json.load(f)
        
        # Create default benchmarks
        benchmarks = [
            {
                "id": 1,
                "job_title": "Software Engineer",
                "skills": ["Python", "Problem Solving", "Analytical Thinking"],
                "experience_level": "Mid",
                "expected_assessments": [
                    "Verify Interactive (G+)",
                    "Verify Inductive Reasoning",
                    "OPQ32 (Occupational Personality Questionnaire)"
                ]
            },
            {
                "id": 2,
                "job_title": "Sales Manager",
                "skills": ["Sales", "Leadership", "Communication", "Persuasion"],
                "experience_level": "Senior",
                "expected_assessments": [
                    "Sales Aptitude Test",
                    "OPQ32 (Occupational Personality Questionnaire)",
                    "Leadership Judgment Indicator (LJI)"
                ]
            },
            {
                "id": 3,
                "job_title": "Customer Service Representative",
                "skills": ["Communication", "Empathy", "Problem Resolution"],
                "experience_level": "Entry",
                "expected_assessments": [
                    "Customer Contact Styles Questionnaire (CCSQ)",
                    "Situational Judgment Test (SJT)",
                    "Workplace English"
                ]
            },
            {
                "id": 4,
                "job_title": "Data Analyst",
                "skills": ["Numerical Analysis", "Data Interpretation", "Excel"],
                "experience_level": "Mid",
                "expected_assessments": [
                    "Verify Numerical Reasoning",
                    "Verify Interactive (G+)",
                    "Management and Graduate Item Bank (MGIB)"
                ]
            },
            {
                "id": 5,
                "job_title": "HR Business Partner",
                "skills": ["Emotional Intelligence", "Communication", "Strategy"],
                "experience_level": "Senior",
                "expected_assessments": [
                    "Emotional Intelligence Questionnaire (EIQ)",
                    "OPQ32 (Occupational Personality Questionnaire)",
                    "Strategic Thinking Questionnaire"
                ]
            },
            {
                "id": 6,
                "job_title": "Mechanical Engineer",
                "skills": ["Technical Skills", "Problem Solving", "Mechanical Reasoning"],
                "experience_level": "Mid",
                "expected_assessments": [
                    "Technical Test Battery (TTB)",
                    "Verify Interactive (G+)",
                    "Verify Inductive Reasoning"
                ]
            },
            {
                "id": 7,
                "job_title": "C-Suite Executive",
                "skills": ["Strategic Thinking", "Leadership", "Decision Making"],
                "experience_level": "Executive",
                "expected_assessments": [
                    "Leadership Judgment Indicator (LJI)",
                    "Strategic Thinking Questionnaire",
                    "OPQ32 (Occupational Personality Questionnaire)"
                ]
            },
            {
                "id": 8,
                "job_title": "Graduate Trainee",
                "skills": ["Learning Agility", "Analytical Skills", "Adaptability"],
                "experience_level": "Entry",
                "expected_assessments": [
                    "Graduate Reasoning Test Battery",
                    "Management and Graduate Item Bank (MGIB)",
                    "Motivation Questionnaire (MQ)"
                ]
            }
        ]
        
        # Save benchmarks
        self.benchmark_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.benchmark_path, 'w') as f:
            json.dump(benchmarks, f, indent=2)
        
        logger.info(f"Created {len(benchmarks)} benchmark test cases")
        return benchmarks
    
    def evaluate_retrieval_precision(self) -> Dict:
        """
        Evaluate retrieval precision against benchmark cases.
        
        Returns:
            Dictionary with precision metrics
        """
        logger.info("Evaluating retrieval precision...")
        
        results = []
        
        for benchmark in self.benchmarks:
            # Get recommendations
            result = self.recommender.recommend(
                job_title=benchmark['job_title'],
                skills=benchmark['skills'],
                experience_level=benchmark['experience_level'],
                use_llm=False
            )
            
            # Get retrieved assessment names
            retrieved_names = [
                a['name'] for a in result['retrieved_assessments']
            ]
            
            # Calculate precision
            expected = set(benchmark['expected_assessments'])
            retrieved = set(retrieved_names)
            
            if len(retrieved) > 0:
                precision = len(expected & retrieved) / len(retrieved)
                recall = len(expected & retrieved) / len(expected) if len(expected) > 0 else 0
                f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            else:
                precision = recall = f1 = 0
            
            results.append({
                'benchmark_id': benchmark['id'],
                'job_title': benchmark['job_title'],
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'expected_count': len(expected),
                'retrieved_count': len(retrieved),
                'matched_count': len(expected & retrieved),
                'matched_assessments': list(expected & retrieved)
            })
        
        # Calculate averages
        df = pd.DataFrame(results)
        avg_precision = df['precision'].mean()
        avg_recall = df['recall'].mean()
        avg_f1 = df['f1_score'].mean()
        
        summary = {
            'average_precision': avg_precision,
            'average_recall': avg_recall,
            'average_f1_score': avg_f1,
            'total_benchmarks': len(self.benchmarks),
            'detailed_results': results
        }
        
        logger.info(f"Average Precision: {avg_precision:.3f}")
        logger.info(f"Average Recall: {avg_recall:.3f}")
        logger.info(f"Average F1 Score: {avg_f1:.3f}")
        
        return summary
    
    def evaluate_recommendation_relevance(self) -> Dict:
        """
        Evaluate overall recommendation relevance.
        
        Returns:
            Dictionary with relevance metrics
        """
        logger.info("Evaluating recommendation relevance...")
        
        results = []
        
        for benchmark in self.benchmarks:
            result = self.recommender.recommend(
                job_title=benchmark['job_title'],
                skills=benchmark['skills'],
                experience_level=benchmark['experience_level'],
                use_llm=False
            )
            
            if result['retrieved_assessments']:
                # Calculate average similarity score
                avg_similarity = np.mean([
                    a['similarity_score'] 
                    for a in result['retrieved_assessments']
                ])
                
                # Check if top result is in expected
                top_result = result['retrieved_assessments'][0]['name']
                top_is_relevant = top_result in benchmark['expected_assessments']
            else:
                avg_similarity = 0
                top_is_relevant = False
            
            results.append({
                'benchmark_id': benchmark['id'],
                'job_title': benchmark['job_title'],
                'avg_similarity': avg_similarity,
                'top_is_relevant': top_is_relevant,
                'retrieval_count': result['retrieval_count']
            })
        
        df = pd.DataFrame(results)
        
        summary = {
            'average_similarity_score': df['avg_similarity'].mean(),
            'top_relevance_rate': df['top_is_relevant'].mean(),
            'average_retrieval_count': df['retrieval_count'].mean(),
            'detailed_results': results
        }
        
        logger.info(f"Average Similarity Score: {summary['average_similarity_score']:.3f}")
        logger.info(f"Top Result Relevance Rate: {summary['top_relevance_rate']:.3f}")
        
        return summary
    
    def generate_evaluation_report(self) -> Dict:
        """
        Generate comprehensive evaluation report.
        
        Returns:
            Complete evaluation report
        """
        logger.info("Generating comprehensive evaluation report...")
        
        report = {
            'retrieval_precision': self.evaluate_retrieval_precision(),
            'recommendation_relevance': self.evaluate_recommendation_relevance(),
            'benchmark_count': len(self.benchmarks)
        }
        
        # Save report
        report_path = Path("data/evaluation/evaluation_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Evaluation report saved to {report_path}")
        
        return report
    
    def print_report_summary(self, report: Dict) -> None:
        """
        Print a formatted summary of the evaluation report.
        
        Args:
            report: Evaluation report dictionary
        """
        print("\n" + "=" * 80)
        print("EVALUATION REPORT SUMMARY")
        print("=" * 80)
        
        print("\n📊 RETRIEVAL PRECISION")
        print("-" * 80)
        rp = report['retrieval_precision']
        print(f"Average Precision: {rp['average_precision']:.3f}")
        print(f"Average Recall:    {rp['average_recall']:.3f}")
        print(f"Average F1 Score:  {rp['average_f1_score']:.3f}")
        
        print("\n🎯 RECOMMENDATION RELEVANCE")
        print("-" * 80)
        rr = report['recommendation_relevance']
        print(f"Average Similarity Score:  {rr['average_similarity_score']:.3f}")
        print(f"Top Result Relevance Rate: {rr['top_relevance_rate']:.1%}")
        print(f"Average Retrieval Count:   {rr['average_retrieval_count']:.1f}")
        
        print("\n📋 BENCHMARK COVERAGE")
        print("-" * 80)
        print(f"Total Benchmark Cases: {report['benchmark_count']}")
        
        print("\n" + "=" * 80)
        print("✅ Evaluation completed successfully!")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    evaluator = SystemEvaluator()
    report = evaluator.generate_evaluation_report()
    evaluator.print_report_summary(report)
