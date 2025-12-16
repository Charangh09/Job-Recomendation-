"""
Assessment Retriever

This module handles semantic search and retrieval of relevant
assessments from the vector database.
"""

import chromadb
from chromadb.config import Settings
from pathlib import Path
import logging
import yaml
from typing import List, Dict, Optional
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.embeddings.embedding_generator import EmbeddingGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssessmentRetriever:
    """
    Retrieves relevant assessments using semantic search.
    
    This class provides efficient similarity-based retrieval
    of assessments from the ChromaDB vector database.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the retriever.
        
        Args:
            config_path: Path to configuration file
        """
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.data_config = config['data_storage']
        self.retrieval_config = config['retrieval']
        self.db_path = Path(self.data_config['vector_db_path'])
        self.collection_name = self.retrieval_config['collection_name']
        self.top_k = self.retrieval_config['top_k']
        # Use lower threshold to ensure we get results
        self.similarity_threshold = 0.1
        
        # Initialize embedding generator
        self.embedding_generator = EmbeddingGenerator(config_path)
        
        # Initialize ChromaDB client
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Vector database not found at {self.db_path}. "
                "Please build the database first."
            )
        
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get collection
        try:
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Connected to collection: {self.collection_name}")
        except Exception as e:
            raise RuntimeError(
                f"Failed to load collection '{self.collection_name}': {e}"
            )
    
    def build_query_text(
        self, 
        job_title: str, 
        skills: List[str], 
        experience_level: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Build a comprehensive query text from user inputs.
        
        Args:
            job_title: Job title or role
            skills: List of required skills
            experience_level: Experience level (Entry/Mid/Senior/Executive)
            additional_context: Optional additional hiring context
            
        Returns:
            Formatted query string
        """
        query_parts = [
            f"Job Title: {job_title}",
            f"Required Skills: {', '.join(skills)}",
            f"Experience Level: {experience_level}"
        ]
        
        if additional_context:
            query_parts.append(f"Context: {additional_context}")
        
        return " | ".join(query_parts)
    
    def retrieve(
        self,
        job_title: str,
        skills: List[str],
        experience_level: str,
        additional_context: Optional[str] = None,
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Retrieve relevant assessments for a job role.
        
        Args:
            job_title: Job title or role
            skills: List of required skills
            experience_level: Experience level
            additional_context: Optional additional context
            top_k: Number of results to retrieve (overrides config)
            
        Returns:
            List of relevant assessment dictionaries
        """
        # Build query
        query_text = self.build_query_text(
            job_title, skills, experience_level, additional_context
        )
        
        logger.info(f"Query: {query_text}")
        
        # Generate query embedding
        query_embedding = self.embedding_generator.encode_query(query_text)
        logger.info(f"Query embedding dimension: {len(query_embedding)}")
        
        # Retrieve from database
        k = top_k if top_k is not None else self.top_k
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        logger.info(f"Raw ChromaDB results: {len(results['documents'][0])} results returned")
        
        # Format results
        assessments = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            # ChromaDB uses cosine distance (can be negative)
            # Convert to similarity score (higher is better)
            similarity_score = 1 - distance
            
            # Don't filter - return all retrieved results
            assessment = {
                'rank': i + 1,
                'name': metadata['name'],
                'category': metadata['category'],
                'description': metadata['description'],
                'skills_measured': metadata['skills_measured'],
                'job_suitability': metadata['job_suitability'],
                'experience_level': metadata['experience_level'],
                'duration': metadata['duration'],
                'delivery_method': metadata['delivery_method'],
                'similarity_score': similarity_score,
                'full_text': doc
            }
            
            assessments.append(assessment)
            logger.debug(f"Result {i+1}: {metadata['name']} - Similarity: {similarity_score:.4f}")
        
        logger.info(f"Retrieved {len(assessments)} relevant assessments")
        return assessments
    
    def search(
        self, 
        query: str, 
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Search for assessments using a query string (alias for retrieve_by_query).
        
        Args:
            query: Search query string
            top_k: Number of results to retrieve
            
        Returns:
            List of relevant assessment dictionaries with 'score' field
        """
        results = self.retrieve_by_query(query, top_k)
        # Add 'score' field for compatibility
        for r in results:
            r['score'] = r.get('similarity_score', 0)
        return results
    
    def retrieve_by_query(
        self, 
        query: str, 
        top_k: Optional[int] = None
    ) -> List[Dict]:
        """
        Retrieve assessments using a free-form query.
        
        Args:
            query: Free-form query string
            top_k: Number of results to retrieve
            
        Returns:
            List of relevant assessment dictionaries
        """
        logger.info(f"Free-form query: {query}")
        
        # Generate query embedding
        query_embedding = self.embedding_generator.encode_query(query)
        
        # Retrieve from database
        k = top_k if top_k is not None else self.top_k
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        # Format results
        assessments = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            similarity_score = 1 - distance
            
            
            assessment = {
                'rank': i + 1,
                'name': metadata['name'],
                'category': metadata['category'],
                'description': metadata['description'],
                'skills_measured': metadata['skills_measured'],
                'job_suitability': metadata['job_suitability'],
                'experience_level': metadata['experience_level'],
                'duration': metadata['duration'],
                'delivery_method': metadata['delivery_method'],
                'assessment_url': metadata.get('assessment_url', ''),
                'similarity_score': similarity_score
            }
            
            assessments.append(assessment)
            logger.debug(f"Result {i+1}: {metadata['name']} - Similarity: {similarity_score:.4f}")
        
        logger.info(f"Retrieved {len(assessments)} relevant assessments")
        return assessments


if __name__ == "__main__":
    # Test retrieval
    retriever = AssessmentRetriever()
    
    # Test 1: Structured query
    print("Test 1: Software Engineer")
    print("=" * 80)
    results = retriever.retrieve(
        job_title="Software Engineer",
        skills=["Python", "Problem Solving", "Team Collaboration"],
        experience_level="Mid"
    )
    
    for result in results:
        print(f"\n{result['rank']}. {result['name']}")
        print(f"   Similarity: {result['similarity_score']:.4f}")
        print(f"   Category: {result['category']}")
        print(f"   Skills: {result['skills_measured'][:100]}...")
    
    # Test 2: Free-form query
    print("\n\n" + "=" * 80)
    print("Test 2: Sales Manager")
    print("=" * 80)
    results = retriever.retrieve_by_query(
        "Sales manager for B2B software with leadership skills"
    )
    
    for result in results:
        print(f"\n{result['rank']}. {result['name']}")
        print(f"   Similarity: {result['similarity_score']:.4f}")
        print(f"   Category: {result['category']}")
