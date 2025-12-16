"""
Embedding Generator

This module generates vector embeddings for assessment descriptions
using sentence transformers for semantic similarity search.
"""

import torch
from sentence_transformers import SentenceTransformer
from typing import List, Union
import logging
import yaml
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """
    Generates embeddings using sentence transformers.
    
    This class handles loading the embedding model and generating
    vector representations of text for semantic search.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the embedding generator.
        
        Args:
            config_path: Path to configuration file
        """
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.embedding_config = config['embedding']
        self.model_name = self.embedding_config['model_name']
        self.batch_size = self.embedding_config['batch_size']
        self.device = self.embedding_config['device']
        
        # Check if CUDA is available
        if self.device == 'cuda' and not torch.cuda.is_available():
            logger.warning("CUDA not available, falling back to CPU")
            self.device = 'cpu'
        
        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name, device=self.device)
        logger.info(f"Model loaded successfully on {self.device}")
    
    def generate_embeddings(
        self, 
        texts: Union[str, List[str]], 
        show_progress: bool = True
    ) -> List[List[float]]:
        """
        Generate embeddings for one or more texts.
        
        Args:
            texts: Single text string or list of texts
            show_progress: Whether to show progress bar
            
        Returns:
            List of embedding vectors
        """
        if isinstance(texts, str):
            texts = [texts]
        
        logger.info(f"Generating embeddings for {len(texts)} texts...")
        
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        logger.info("Embeddings generated successfully")
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimensionality of the embeddings.
        
        Returns:
            Embedding dimension
        """
        return self.model.get_sentence_embedding_dimension()
    
    def encode_query(self, query: str) -> List[float]:
        """
        Encode a single query for retrieval.
        
        Args:
            query: Query text
            
        Returns:
            Query embedding vector
        """
        # Debug: Log the query being encoded
        logger.debug(f"Encoding query: {query[:100]}...")
        
        embedding = self.model.encode(
            query, 
            convert_to_numpy=True
        )
        
        # Debug: Log the embedding hash for verification
        embedding_hash = hash(tuple(embedding[:5]))
        logger.debug(f"Embedding generated (hash: {embedding_hash})")
        
        return embedding.tolist()


if __name__ == "__main__":
    # Test the embedding generator
    generator = EmbeddingGenerator()
    
    test_texts = [
        "Software engineer with Python experience",
        "Sales representative for B2B software",
        "Customer service manager with team leadership"
    ]
    
    embeddings = generator.generate_embeddings(test_texts)
    print(f"Generated {len(embeddings)} embeddings")
    print(f"Embedding dimension: {generator.get_embedding_dimension()}")
    print(f"First embedding shape: {len(embeddings[0])}")
