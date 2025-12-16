"""
Assessment Recommender

This module implements the RAG (Retrieval-Augmented Generation) pipeline
for generating assessment recommendations with explanations using LLMs.
"""

import os
from typing import List, Dict, Optional
import logging
import yaml
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
import pandas as pd

from src.retrieval.retriever import AssessmentRetriever
from openai import OpenAI
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssessmentRecommender:
    """
    RAG-based assessment recommendation engine.
    
    This class combines semantic retrieval with LLM reasoning
    to generate contextualized, explained recommendations.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the recommender.
        
        Args:
            config_path: Path to configuration file
        """
        # Load environment variables with explicit path
        env_path = Path(__file__).parent.parent.parent / ".env"
        load_dotenv(env_path)
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.llm_config = config['llm']
        self.retrieval_config = config['retrieval']
        
        # Initialize retriever
        self.retriever = AssessmentRetriever(config_path)
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning(
                "OPENAI_API_KEY not found. LLM recommendations will not work. "
                "Set the key in your .env file."
            )
            self.client = None
        else:
            try:
                # Remove any proxy environment variables to avoid conflicts
                os.environ.pop('HTTP_PROXY', None)
                os.environ.pop('HTTPS_PROXY', None)
                os.environ.pop('http_proxy', None)
                os.environ.pop('https_proxy', None)
                
                self.client = OpenAI(api_key=api_key)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    def _format_assessment_for_context(self, assessment: Dict) -> str:
        """
        Format an assessment for inclusion in LLM context.
        
        Args:
            assessment: Assessment dictionary
            
        Returns:
            Formatted string representation
        """
        return f"""
Assessment: {assessment['name']}
Category: {assessment['category']}
Description: {assessment['description']}
Skills Measured: {assessment['skills_measured']}
Job Suitability: {assessment['job_suitability']}
Experience Levels: {assessment['experience_level']}
Duration: {assessment['duration']}
Relevance Score: {assessment['similarity_score']:.2f}
"""
    
    def _build_llm_prompt(
        self,
        job_title: str,
        skills: List[str],
        experience_level: str,
        additional_context: Optional[str],
        retrieved_assessments: List[Dict]
    ) -> str:
        """
        Build the prompt for the LLM.
        
        Args:
            job_title: Job title
            skills: Required skills
            experience_level: Experience level
            additional_context: Additional context
            retrieved_assessments: Retrieved assessments
            
        Returns:
            Formatted prompt string
        """
        # Format retrieved assessments
        assessments_context = "\n---\n".join([
            self._format_assessment_for_context(a) 
            for a in retrieved_assessments
        ])
        
        prompt = f"""You are an expert HR technology consultant specializing in SHL assessment products.

HIRING REQUIREMENTS:
- Job Title: {job_title}
- Required Skills: {', '.join(skills)}
- Experience Level: {experience_level}
{f'- Additional Context: {additional_context}' if additional_context else ''}

AVAILABLE SHL ASSESSMENTS (from catalog):
{assessments_context}

TASK:
Based ONLY on the assessments provided above, recommend the top 3-5 most suitable SHL assessments for this role. For each recommendation:

1. State the assessment name
2. Explain why it's relevant for this specific role
3. Highlight which skills/competencies it addresses from the requirements
4. Mention any important considerations (duration, experience level match, etc.)

Format your response as a numbered list with clear explanations. Be specific and practical. Only recommend assessments from the provided catalog above.
"""
        return prompt
    
    def recommend(
        self,
        job_title: str,
        skills: List[str],
        experience_level: str = "Mid",
        additional_context: Optional[str] = None,
        use_llm: bool = True
    ) -> Dict:
        """
        Generate assessment recommendations for a job role.
        
        Args:
            job_title: Job title or role
            skills: List of required skills
            experience_level: Experience level
            additional_context: Optional additional context
            use_llm: Whether to use LLM for explanations
            
        Returns:
            Dictionary containing recommendations and metadata
        """
        logger.info(f"Generating recommendations for: {job_title}")
        
        # Step 1: Retrieve relevant assessments
        retrieved_assessments = self.retriever.retrieve(
            job_title=job_title,
            skills=skills,
            experience_level=experience_level,
            additional_context=additional_context
        )
        
        if not retrieved_assessments:
            return {
                'job_title': job_title,
                'skills': skills,
                'experience_level': experience_level,
                'retrieved_assessments': [],
                'recommendations': [],
                'explanation': "No suitable assessments found for the given criteria.",
                'retrieval_count': 0,
                'llm_recommendations': None
            }
        
        # Step 2: Generate LLM-based recommendations if enabled
        llm_response = None
        if use_llm and self.client:
            try:
                prompt = self._build_llm_prompt(
                    job_title, skills, experience_level, 
                    additional_context, retrieved_assessments
                )
                
                response = self.client.chat.completions.create(
                    model=self.llm_config['model'],
                    messages=[
                        {"role": "system", "content": self.llm_config['system_prompt']},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.llm_config['temperature'],
                    max_tokens=self.llm_config['max_tokens']
                )
                
                llm_response = response.choices[0].message.content
                logger.info("LLM recommendations generated successfully")
                
            except Exception as e:
                logger.error(f"Error generating LLM recommendations: {e}")
                llm_response = None
        
        # Format response
        result = {
            'job_title': job_title,
            'skills': skills,
            'experience_level': experience_level,
            'additional_context': additional_context,
            'retrieved_assessments': retrieved_assessments,
            'llm_recommendations': llm_response,
            'retrieval_count': len(retrieved_assessments),
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        return result
    
    def recommend_simple(
        self,
        query: str,
        use_llm: bool = True
    ) -> Dict:
        """
        Generate recommendations from a simple query string.
        
        Args:
            query: Free-form query describing the role
            use_llm: Whether to use LLM for explanations
            
        Returns:
            Dictionary containing recommendations
        """
        logger.info(f"Generating recommendations for query: {query}")
        
        # Retrieve relevant assessments
        retrieved_assessments = self.retriever.retrieve_by_query(query)
        
        if not retrieved_assessments:
            return {
                'query': query,
                'recommendations': [],
                'explanation': "No suitable assessments found.",
                'retrieval_count': 0
            }
        
        # Generate LLM recommendations if enabled
        llm_response = None
        if use_llm and self.client:
            try:
                assessments_context = "\n---\n".join([
                    self._format_assessment_for_context(a)
                    for a in retrieved_assessments
                ])
                
                prompt = f"""You are an expert HR technology consultant specializing in SHL assessment products.

HIRING QUERY: {query}

AVAILABLE SHL ASSESSMENTS (from catalog):
{assessments_context}

TASK:
Based ONLY on the assessments provided above, recommend the top 3-5 most suitable SHL assessments. For each recommendation:

1. State the assessment name
2. Explain why it's relevant
3. Highlight key competencies it measures
4. Mention important considerations

Format as a numbered list. Only recommend assessments from the provided catalog.
"""
                
                response = self.client.chat.completions.create(
                    model=self.llm_config['model'],
                    messages=[
                        {"role": "system", "content": self.llm_config['system_prompt']},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.llm_config['temperature'],
                    max_tokens=self.llm_config['max_tokens']
                )
                
                llm_response = response.choices[0].message.content
                logger.info("LLM recommendations generated successfully")
                
            except Exception as e:
                logger.error(f"Error generating LLM recommendations: {e}")
                llm_response = None
        
        return {
            'query': query,
            'retrieved_assessments': retrieved_assessments,
            'llm_recommendations': llm_response,
            'retrieval_count': len(retrieved_assessments)
        }


if __name__ == "__main__":
    recommender = AssessmentRecommender()
    
    # Test recommendation
    result = recommender.recommend(
        job_title="Senior Software Engineer",
        skills=["Python", "Problem Solving", "Team Leadership", "System Design"],
        experience_level="Senior",
        additional_context="Looking for technical and leadership capabilities"
    )
    
    print("\n" + "=" * 80)
    print(f"RECOMMENDATIONS FOR: {result['job_title']}")
    print("=" * 80)
    
    print(f"\nRetrieved {result['retrieval_count']} relevant assessments")
    
    print("\n--- Top Retrieved Assessments ---")
    for assessment in result['retrieved_assessments'][:3]:
        print(f"\n{assessment['rank']}. {assessment['name']}")
        print(f"   Score: {assessment['similarity_score']:.3f}")
        print(f"   Category: {assessment['category']}")
    
    if result['llm_recommendations']:
        print("\n--- LLM-Generated Recommendations ---")
        print(result['llm_recommendations'])
