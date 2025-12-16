"""
Vector Database Builder

This module builds and manages a ChromaDB vector database
for efficient semantic search of SHL assessments.
"""

import chromadb
from chromadb.config import Settings
import pandas as pd
from pathlib import Path
import logging
import yaml
from typing import List, Dict, Optional
import uuid

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.embeddings.embedding_generator import EmbeddingGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorDBBuilder:
    """
    Builds and manages ChromaDB vector database for assessments.
    
    This class handles creating embeddings for all assessments
    and storing them in ChromaDB for efficient retrieval.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the vector database builder.
        
        Args:
            config_path: Path to configuration file
        """
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.data_config = config['data_storage']
        self.retrieval_config = config['retrieval']
        self.db_path = Path(self.data_config['vector_db_path'])
        self.collection_name = self.retrieval_config['collection_name']
        
        # Initialize embedding generator
        self.embedding_generator = EmbeddingGenerator(config_path)
        
        # Initialize ChromaDB client
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        logger.info(f"ChromaDB initialized at {self.db_path}")
    
    def load_processed_data(self) -> pd.DataFrame:
        """
        Load processed assessment data.
        
        Returns:
            DataFrame with processed assessments
        """
        data_path = Path(self.data_config['processed_data_path'])
        
        if not data_path.exists():
            raise FileNotFoundError(
                f"Processed data not found: {data_path}. "
                "Please run the parser first."
            )
        
        df = pd.read_csv(data_path, encoding='utf-8')
        logger.info(f"Loaded {len(df)} assessments from {data_path}")
        return df
    
    def create_collection(self, reset: bool = False) -> chromadb.Collection:
        """
        Create or get ChromaDB collection.
        
        Args:
            reset: Whether to delete existing collection
            
        Returns:
            ChromaDB collection
        """
        if reset:
            try:
                self.client.delete_collection(self.collection_name)
                logger.info(f"Deleted existing collection: {self.collection_name}")
            except Exception as e:
                logger.info(f"No existing collection to delete: {e}")
        
        collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "SHL Assessment Catalog"}
        )
        
        logger.info(f"Collection '{self.collection_name}' ready")
        return collection
    
    def build_database(self, reset: bool = False) -> None:
        """
        Build the complete vector database.
        
        This method:
        1. Loads processed assessment data
        2. Generates embeddings for all assessments
        3. Stores in ChromaDB with metadata
        
        Args:
            reset: Whether to rebuild from scratch
        """
        logger.info("Starting vector database build...")
        
        # Load data
        df = self.load_processed_data()
        
        # Create collection
        collection = self.create_collection(reset=reset)
        
        # Generate embeddings
        logger.info("Generating embeddings for all assessments...")
        embeddings = self.embedding_generator.generate_embeddings(
            df['full_text'].tolist(),
            show_progress=True
        )
        
        # Prepare data for ChromaDB
        ids = [str(uuid.uuid4()) for _ in range(len(df))]
        documents = df['full_text'].tolist()
        metadatas = df.drop('full_text', axis=1).to_dict('records')
        
        # Add to collection
        logger.info("Adding assessments to vector database...")
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        
        logger.info(f"Successfully added {len(df)} assessments to vector database")
        logger.info(f"Database location: {self.db_path}")
    
    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            collection = self.client.get_collection(self.collection_name)
            count = collection.count()
            
            return {
                'collection_name': self.collection_name,
                'document_count': count,
                'db_path': str(self.db_path)
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    def test_retrieval(self, query: str, top_k: int = 3) -> None:
        """
        Test retrieval with a sample query.
        
        Args:
            query: Test query string
            top_k: Number of results to retrieve
        """
        logger.info(f"Testing retrieval with query: '{query}'")
        
        collection = self.client.get_collection(self.collection_name)
        query_embedding = self.embedding_generator.encode_query(query)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        print(f"\nTop {top_k} results for: '{query}'")
        print("=" * 80)
        
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ), 1):
            print(f"\n{i}. {metadata['name']}")
            print(f"   Category: {metadata['category']}")
            print(f"   Similarity: {1 - distance:.4f}")
            print(f"   Description: {metadata['description'][:100]}...")


if __name__ == "__main__":
    builder = VectorDBBuilder()
    
    # Build database
    builder.build_database(reset=True)
    
    # Show stats
    stats = builder.get_collection_stats()
    print("\nDatabase Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test retrieval
    print("\n" + "=" * 80)
    builder.test_retrieval("Software engineer with Python skills", top_k=3)
    print("\n" + "=" * 80)
    builder.test_retrieval("Sales manager for B2B software", top_k=3)
