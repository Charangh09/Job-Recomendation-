"""
SHL Evaluation Framework - Mean Recall@K

Evaluates recommendation system against labeled training dataset.
Implements Mean Recall@K metric as specified in SHL assignment requirements.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Tuple
import logging
import numpy as np
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MeanRecallAtKEvaluator:
    """
    Evaluator implementing Mean Recall@K metric.
    
    For each query:
        - Get top-K recommendations from system
        - Compare against ground truth assessments
        - Calculate Recall@K = (# correct in top-K) / (# ground truth assessments)
    
    Mean Recall@K = Average Recall@K across all queries
    """
    
    def __init__(self, K_values: List[int] = [5, 10]):
        """
        Initialize evaluator.
        
        Args:
            K_values: K values to evaluate at (default: [5, 10])
        """
        self.K_values = K_values
        self.results = {}
        
    def load_training_data(self, filepath: str) -> Dict[str, List[str]]:
        """
        Load labeled training dataset.
        
        Expected format: CSV or JSON with:
        - query_id / query: The query or job description
        - assessment_urls / assessments: List of relevant assessment URLs
        
        Args:
            filepath: Path to training data file
            
        Returns:
            Dictionary mapping query_id to list of ground truth URLs
        """
        ground_truth = {}
        
        try:
            if filepath.endswith('.csv'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        query_id = row.get('Query') or row.get('query_id') or row.get('query')
                        urls = row.get('Assessment_URLs') or row.get('assessments') or row.get('assessment_urls')
                        
                        if query_id and urls:
                            # Handle both comma-separated and JSON list formats
                            if isinstance(urls, str):
                                if urls.startswith('['):
                                    urls = json.loads(urls)
                                else:
                                    urls = [u.strip() for u in urls.split(',')]
                            ground_truth[query_id] = urls
                            
            elif filepath.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    if isinstance(data, list):
                        for item in data:
                            query_id = item.get('query_id') or item.get('id')
                            urls = item.get('assessment_urls') or item.get('assessments')
                            if query_id and urls:
                                ground_truth[query_id] = urls if isinstance(urls, list) else [urls]
                    elif isinstance(data, dict):
                        ground_truth = data
            
            logger.info(f"Loaded {len(ground_truth)} labeled queries from training data")
            return ground_truth
            
        except Exception as e:
            logger.error(f"Failed to load training data: {e}")
            return {}
    
    def calculate_recall_at_k(
        self,
        predicted: List[str],
        ground_truth: List[str],
        k: int
    ) -> float:
        """
        Calculate Recall@K for a single query.
        
        Recall@K = (# correct assessments in top-K predictions) / (# ground truth assessments)
        
        Args:
            predicted: List of predicted assessment URLs (ranked)
            ground_truth: List of ground truth assessment URLs
            k: K value to evaluate at
            
        Returns:
            Recall@K score (0.0 to 1.0)
        """
        if not ground_truth:
            return 1.0  # Perfect score if no ground truth (edge case)
        
        # Get top-K predictions
        top_k = set(predicted[:k])
        ground_truth_set = set(ground_truth)
        
        # Count matches
        correct = len(top_k & ground_truth_set)
        
        # Calculate recall
        recall = correct / len(ground_truth_set)
        return recall
    
    def evaluate_system(
        self,
        query_predictions: Dict[str, List[str]],
        ground_truth: Dict[str, List[str]],
        verbose: bool = True
    ) -> Dict:
        """
        Evaluate recommendation system against ground truth.
        
        Args:
            query_predictions: Dict mapping query_id to list of predicted URLs
            ground_truth: Dict mapping query_id to list of ground truth URLs
            verbose: Whether to print detailed results
            
        Returns:
            Evaluation results dictionary
        """
        results = {
            'queries_evaluated': 0,
            'mean_recall_at_k': {},
            'per_query_recall': defaultdict(dict),
            'summary': {}
        }
        
        # Calculate Recall@K for each query
        for query_id, ground_truth_urls in ground_truth.items():
            if query_id not in query_predictions:
                logger.warning(f"No predictions found for query: {query_id}")
                continue
            
            predicted_urls = query_predictions[query_id]
            results['queries_evaluated'] += 1
            
            # Calculate for each K
            for k in self.K_values:
                recall = self.calculate_recall_at_k(predicted_urls, ground_truth_urls, k)
                
                if f'recall@{k}' not in results['mean_recall_at_k']:
                    results['mean_recall_at_k'][f'recall@{k}'] = []
                
                results['mean_recall_at_k'][f'recall@{k}'].append(recall)
                results['per_query_recall'][query_id][f'recall@{k}'] = recall
        
        # Calculate mean values
        for k_metric, recalls in results['mean_recall_at_k'].items():
            if recalls:
                mean = np.mean(recalls)
                std = np.std(recalls)
                min_val = np.min(recalls)
                max_val = np.max(recalls)
                
                results['summary'][k_metric] = {
                    'mean': round(float(mean), 4),
                    'std': round(float(std), 4),
                    'min': round(float(min_val), 4),
                    'max': round(float(max_val), 4)
                }
                
                if verbose:
                    logger.info(f"{k_metric}: {mean:.4f} ± {std:.4f}")
        
        return dict(results)
    
    def generate_predictions_csv(
        self,
        output_file: str,
        predictions: Dict[str, List[Dict]],
        query_mapping: Dict[str, str] = None
    ):
        """
        Generate predictions CSV in exact SHL format (Appendix 3).
        
        Format:
        Query, Assessment_URL
        query_1, https://shl.com/assessment/1
        query_1, https://shl.com/assessment/2
        ...
        
        Args:
            output_file: Path to save CSV
            predictions: Dict mapping query_id to list of assessment dicts
            query_mapping: Optional mapping of query_id to query text
        """
        try:
            rows = []
            
            for query_id, assessments in predictions.items():
                # Use query_id as first column (or mapped text)
                query_display = query_mapping.get(query_id, query_id) if query_mapping else query_id
                
                # One row per recommended assessment
                for assessment in assessments:
                    url = assessment.get('url') or assessment.get('assessment_url')
                    if url:
                        rows.append({
                            'Query': query_display,
                            'Assessment_URL': url
                        })
            
            # Write CSV
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['Query', 'Assessment_URL'])
                writer.writeheader()
                writer.writerows(rows)
            
            logger.info(f"Saved {len(rows)} predictions to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Failed to save predictions: {e}")
            return None
    
    def generate_evaluation_report(
        self,
        evaluation_results: Dict,
        output_file: str
    ):
        """
        Generate detailed evaluation report.
        
        Args:
            evaluation_results: Results from evaluate_system()
            output_file: Path to save report
        """
        try:
            report = []
            report.append("=" * 80)
            report.append("SHL ASSESSMENT RECOMMENDATION SYSTEM - EVALUATION REPORT")
            report.append("Mean Recall@K Metric")
            report.append("=" * 80)
            report.append("")
            
            # Summary statistics
            report.append("SUMMARY")
            report.append("-" * 80)
            report.append(f"Queries Evaluated: {evaluation_results['queries_evaluated']}")
            report.append("")
            
            for metric, stats in evaluation_results['summary'].items():
                report.append(f"{metric}:")
                report.append(f"  Mean:  {stats['mean']:.4f}")
                report.append(f"  Std:   {stats['std']:.4f}")
                report.append(f"  Min:   {stats['min']:.4f}")
                report.append(f"  Max:   {stats['max']:.4f}")
                report.append("")
            
            # Per-query results
            report.append("")
            report.append("PER-QUERY RESULTS")
            report.append("-" * 80)
            for query_id, recalls in evaluation_results['per_query_recall'].items():
                report.append(f"{query_id}:")
                for metric, value in recalls.items():
                    report.append(f"  {metric}: {value:.4f}")
            
            report.append("")
            report.append("=" * 80)
            
            # Save report
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report))
            
            logger.info(f"Saved evaluation report to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return None


class EvaluationPipeline:
    """
    Complete evaluation pipeline from training data to report.
    """
    
    def __init__(self, recommender):
        """
        Initialize pipeline.
        
        Args:
            recommender: AssessmentRecommender instance
        """
        self.recommender = recommender
        self.evaluator = MeanRecallAtKEvaluator()
    
    def run_full_evaluation(
        self,
        training_data_file: str,
        test_data_file: str = None,
        output_dir: str = "evaluation_results"
    ) -> Dict:
        """
        Run complete evaluation pipeline:
        1. Load and parse training data
        2. Generate predictions for training queries
        3. Calculate Mean Recall@K
        4. Generate test predictions (if provided)
        5. Create evaluation report
        
        Args:
            training_data_file: Path to labeled training data
            test_data_file: Path to unlabeled test data (optional)
            output_dir: Directory to save results
            
        Returns:
            Evaluation results dictionary
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info("Starting full evaluation pipeline...")
        
        # Load training data
        ground_truth = self.evaluator.load_training_data(training_data_file)
        if not ground_truth:
            logger.error("No training data loaded")
            return {}
        
        # Generate predictions for training queries
        logger.info(f"Generating predictions for {len(ground_truth)} training queries...")
        query_predictions = {}
        
        for query_id, urls in ground_truth.items():
            # Assume query_id can be used as query text or needs mapping
            predictions = self.recommender.recommend_simple(query_id, top_k=10)
            query_predictions[query_id] = [
                p.get('url') or p.get('assessment_url') for p in predictions
            ]
        
        # Evaluate
        logger.info("Calculating Mean Recall@K...")
        results = self.evaluator.evaluate_system(query_predictions, ground_truth)
        
        # Save training predictions
        pred_file = Path(output_dir) / "training_predictions.csv"
        self.evaluator.generate_predictions_csv(
            str(pred_file),
            query_predictions
        )
        
        # Generate test predictions if provided
        if test_data_file:
            logger.info("Generating test predictions...")
            test_predictions = self._generate_test_predictions(test_data_file)
            
            test_pred_file = Path(output_dir) / "test_predictions.csv"
            self.evaluator.generate_predictions_csv(
                str(test_pred_file),
                test_predictions
            )
        
        # Generate report
        report_file = Path(output_dir) / "evaluation_report.txt"
        self.evaluator.generate_evaluation_report(results, str(report_file))
        
        logger.info(f"Evaluation complete. Results saved to {output_dir}")
        return results
    
    def _generate_test_predictions(self, test_file: str) -> Dict:
        """Generate predictions for test queries."""
        test_data = self.evaluator.load_training_data(test_file)
        test_predictions = {}
        
        for query_id in test_data.keys():
            predictions = self.recommender.recommend_simple(query_id, top_k=10)
            test_predictions[query_id] = predictions
        
        return test_predictions


def evaluate_recommendation_system(
    recommender,
    training_data_path: str = "data/labeled_training_data.csv",
    test_data_path: str = None
) -> Dict:
    """
    Main evaluation function.
    
    Args:
        recommender: AssessmentRecommender instance
        training_data_path: Path to training data
        test_data_path: Path to test data (optional)
        
    Returns:
        Evaluation results
    """
    pipeline = EvaluationPipeline(recommender)
    return pipeline.run_full_evaluation(
        training_data_path,
        test_data_path,
        output_dir="evaluation_results"
    )


if __name__ == "__main__":
    # Example usage
    from src.recommendation.recommender import AssessmentRecommender
    
    recommender = AssessmentRecommender()
    results = evaluate_recommendation_system(
        recommender,
        training_data_path="data/training_data.csv"
    )
    
    print("\nEvaluation Results:")
    print(json.dumps(results['summary'], indent=2))
