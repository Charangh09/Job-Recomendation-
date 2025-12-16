#!/usr/bin/env python
"""
Test script to verify that different queries return different results.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.recommendation.recommender import AssessmentRecommender

def test_different_queries():
    """Test that different queries return different results."""
    
    recommender = AssessmentRecommender()
    
    test_cases = [
        {
            "job_title": "Software Engineer",
            "skills": ["Python", "Problem Solving"],
            "experience_level": "Entry"
        },
        {
            "job_title": "Sales Manager",
            "skills": ["Communication", "Leadership"],
            "experience_level": "Senior"
        },
        {
            "job_title": "Data Analyst",
            "skills": ["Statistics", "SQL", "Analytics"],
            "experience_level": "Mid"
        },
        {
            "job_title": "HR Manager",
            "skills": ["People Management", "Recruitment"],
            "experience_level": "Senior"
        }
    ]
    
    print("=" * 80)
    print("TESTING DIFFERENT QUERIES FOR DIFFERENT RESULTS")
    print("=" * 80)
    
    previous_results = None
    all_same = True
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\n[Test {idx}]")
        print(f"Job Title: {test_case['job_title']}")
        print(f"Skills: {', '.join(test_case['skills'])}")
        print(f"Experience Level: {test_case['experience_level']}")
        
        result = recommender.recommend(
            job_title=test_case['job_title'],
            skills=test_case['skills'],
            experience_level=test_case['experience_level'],
            use_llm=False
        )
        
        assessments = result['retrieved_assessments']
        print(f"Retrieved {len(assessments)} assessments:")
        
        current_results = []
        for i, assessment in enumerate(assessments[:5], 1):
            print(f"  {i}. {assessment['name']} (Score: {assessment['similarity_score']:.4f})")
            current_results.append((assessment['name'], assessment['similarity_score']))
        
        if previous_results:
            if current_results == previous_results:
                print("  ⚠️  SAME AS PREVIOUS QUERY - POSSIBLE CACHING ISSUE!")
                all_same = True
            else:
                print("  ✓ Different from previous query")
                all_same = False
        
        previous_results = current_results
    
    print("\n" + "=" * 80)
    if all_same:
        print("⚠️  WARNING: Same results for multiple queries - caching may be active!")
    else:
        print("✓ SUCCESS: Different queries returning different results!")
    print("=" * 80)

if __name__ == "__main__":
    test_different_queries()
