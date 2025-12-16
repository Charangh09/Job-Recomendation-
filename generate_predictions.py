"""
Generate predictions for test dataset
"""
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.retrieval.retriever import AssessmentRetriever

def generate_predictions():
    """Generate predictions for all queries in the dataset."""
    
    # Load the assessments data
    df = pd.read_csv('data/processed/assessments.csv')
    
    # Extract unique queries from the description column
    # The description contains the original query
    queries = df['description'].unique()
    
    # Initialize retriever
    print("Initializing retriever...")
    retriever = AssessmentRetriever()
    
    # Generate predictions
    results = []
    for idx, query in enumerate(queries, 1):
        print(f"Processing {idx}/{len(queries)}: {query[:50]}...")
        
        # Get top 5 recommendations
        recommendations = retriever.search(query, top_k=5)
        
        # Get the top assessment URL
        if recommendations:
            top_assessment = recommendations[0].get('assessment_url', '')
            top_name = recommendations[0].get('name', '')
            score = recommendations[0].get('similarity_score', 0.0)
        else:
            top_assessment = ''
            top_name = ''
            score = 0.0
        
        results.append({
            'query': query,
            'predicted_assessment': top_name,
            'predicted_url': top_assessment,
            'confidence_score': score
        })
    
    # Create DataFrame
    predictions_df = pd.DataFrame(results)
    
    # Save to CSV
    output_file = 'sricharan_sirikonda.csv'
    predictions_df.to_csv(output_file, index=False)
    print(f"\n✅ Predictions saved to {output_file}")
    print(f"Total predictions: {len(predictions_df)}")
    
    return predictions_df

if __name__ == '__main__':
    predictions = generate_predictions()
    print("\nFirst 5 predictions:")
    print(predictions.head())
